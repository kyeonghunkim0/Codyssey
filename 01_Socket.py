# python3 01_Socket.py --host 127.0.0.1 --port 5000
# nc 127.0.0.1 5000

from __future__ import annotations

import argparse
import socket
import threading
from typing import Dict, Optional, Tuple


ENCODING = 'utf-8'
BUFFER_SIZE = 4096
WELCOME_PROMPT = '닉네임을 입력하세요: '
QUIT_COMMAND = '/종료'
WHISPER_ALIASES = {'/w', '/whisper', '/귓속말'}
COMMAND_PREFIX = '/'


class ChatServer:
    """멀티스레드 TCP 채팅 서버."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        # 빠른 재시작을 위해 SO_REUSEADDR 활성화
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # socket Option
        self._clients_lock = threading.Lock()
        # 클라이언트 소켓 -> 닉네임 매핑
        self._clients: Dict[socket.socket, str] = {}
        self._user_seq = 0

    def start(self) -> None:
        """서버를 시작하고 접속 대기 루프에 진입한다."""
        self._sock.bind((self.host, self.port))
        self._sock.listen() # OS 요청
        print(f'[INFO] ChatServer listening on {self.host}:{self.port}')

        try:
            while True:
                conn, addr = self._sock.accept()
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()
        except KeyboardInterrupt:
            print('\n[INFO] KeyboardInterrupt: shutting down.')
        finally:
            self._shutdown()

    # ------------------------------
    # Utilities
    # ------------------------------
    def _register_client(self, conn: socket.socket, nickname: str) -> None:
        with self._clients_lock:
            self._clients[conn] = nickname

    def _unregister_client(self, conn: socket.socket) -> Optional[str]:
        with self._clients_lock:
            return self._clients.pop(conn, None)

    def _broadcast(self, message: str, exclude: Optional[socket.socket] = None) -> None:
        """모든 클라이언트에 메시지를 전송. 실패한 소켓은 정리"""
        to_remove = []
        data = (message + '\n').encode(ENCODING, errors='ignore')
        with self._clients_lock:
            for client in list(self._clients.keys()):
                if exclude is not None and client is exclude:
                    continue
                try:
                    client.sendall(data)
                except OSError:
                    to_remove.append(client)
        for dead in to_remove:
            nickname = self._unregister_client(dead)
            try:
                dead.close()
            except OSError:
                pass
            if nickname:
                self._broadcast(f'{nickname}님이 연결이 끊어졌습니다.')

    def _safe_send(self, conn: socket.socket, text: str) -> None:
        try:
            conn.sendall(text.encode(ENCODING, errors='ignore'))
        except OSError:
            pass

    def _normalize_text(self, text: str) -> str:
        """제어문자 제거 및 앞뒤 공백 제거."""
        cleaned = ''.join(ch for ch in text if (ch.isprintable() or ch in ('\t', ' ')))
        return cleaned.strip()

    def _is_quit(self, text: str) -> bool:
        """종료 명령 별칭 지원."""
        norm = self._normalize_text(text)
        if not norm.startswith('/'):
            return False
        return norm == '/종료'

    def _name_in_use(self, nickname: str) -> bool:
        with self._clients_lock:
            return nickname in self._clients.values()

    def _unique_nickname(self, base: str) -> str:
        """중복 닉네임이 있으면 숫자를 붙여 유일하게 만든다."""
        name = base
        n = 1
        while self._name_in_use(name):
            name = f'{base}{n}'
            n += 1
        return name

    def _send_to_nickname(self, sender: str, target_name: str, message: str) -> bool:
        """특정 닉네임에게만 비공개 메시지 전송. 성공 여부 반환."""
        target_sock = None
        with self._clients_lock:
            for sock, nick in self._clients.items():
                if nick == target_name:
                    target_sock = sock
                    break
        if target_sock is None:
            return False
        body = f'(귓속말){sender}> {message}\n'.encode(ENCODING, errors='ignore')
        try:
            target_sock.sendall(body)
        except OSError:
            return False
        return True

    def _try_handle_command(self, nickname: str, raw: str) -> bool:
        """명령어를 처리한다. 처리했으면 True, 아니면 False 반환."""
        text = self._normalize_text(raw)
        if not text.startswith(COMMAND_PREFIX):
            return False
        # 종료 명령은 상위에서 처리하므로 여기서는 귓속말만 처리
        parts = text.split(maxsplit=2)
        if not parts:
            return False
        cmd = parts[0]
        # 귓속말: /w 닉네임 메시지
        if cmd in WHISPER_ALIASES:
            if len(parts) < 3:
                # 형식 안내
                with self._clients_lock:
                    for sock, nick in self._clients.items():
                        if nick == nickname:
                            self._safe_send(sock, "사용법) /w 대상닉 메시지\n")
                            break
                return True
            target = parts[1]
            msg = parts[2]
            if target == nickname:
                with self._clients_lock:
                    for sock, nick in self._clients.items():
                        if nick == nickname:
                            self._safe_send(sock, '자기 자신에게는 귓속말을 보낼 수 없습니다.\n')
                            break
                return True
            ok = self._send_to_nickname(nickname, target, msg)
            if not ok:
                with self._clients_lock:
                    for sock, nick in self._clients.items():
                        if nick == nickname:
                            self._safe_send(sock, f"대상 '{target}' 닉네임을 찾을 수 없습니다.\n")
                            break
            return True
        return False
    # 받기
    def _recv_line(self, conn: socket.socket) -> Optional[str]:
        """개행 기준으로 한 줄을 수신한다. 연결 종료 시 None 반환."""
        chunks: list[bytes] = []
        while True:
            try:
                buf = conn.recv(BUFFER_SIZE)
            except OSError:
                return None
            if not buf:
                return None
            chunks.append(buf)
            if b'\n' in buf:
                break
        try:
            line = b''.join(chunks).decode(ENCODING, errors='ignore')
        except UnicodeDecodeError:
            return ''
        return line.strip('\r\n')

    def _next_default_name(self) -> str:
        self._user_seq += 1
        return f'사용자{self._user_seq}'
    # 닉네임
    def _negotiate_nickname(self, conn: socket.socket) -> str:
        self._safe_send(conn, WELCOME_PROMPT)
        nick = self._recv_line(conn)
        if not nick:
            return self._next_default_name()
        nick = nick.strip()
        if not nick:
            return self._next_default_name()
        # 공백 정리 및 너무 긴 닉네임 제한 후, 중복이면 숫자 부여
        nick = ' '.join(nick.split())[:30]
        nick = nick or self._next_default_name()
        return self._unique_nickname(nick)
    # 통신
    def _handle_client(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        peer = f'{addr[0]}:{addr[1]}'
        try:
            nickname = self._negotiate_nickname(conn)
            self._register_client(conn, nickname)
            self._broadcast(f'{nickname}님이 입장하셨습니다.')
            self._safe_send(conn, "안내) '/종료' 또는 '/quit' 로 종료, 귓속말은 '/w 닉 메시지' 입니다.\n")

            while True:
                line = self._recv_line(conn)
                if line is None:
                    break
                if not line:
                    continue

                # 종료 명령 우선 처리
                if self._is_quit(line):
                    break

                # 명령어 처리(귓속말 등). 처리되면 다음 루프
                if self._try_handle_command(nickname, line):
                    continue

                # 일반 메시지 방송(제어문자 제거)
                sanitized = self._normalize_text(line)
                if sanitized:
                    self._broadcast(f'{nickname}> {sanitized}')
        except Exception as exc:  # pylint: disable=broad-except
            print(f'[WARN] client {peer} error: {exc!r}')
        finally:
            gone = self._unregister_client(conn)
            try:
                conn.close()
            except OSError:
                pass
            if gone:
                self._broadcast(f'{gone}님이 퇴장하셨습니다.')

    def _shutdown(self) -> None:
        with self._clients_lock:
            for conn in list(self._clients.keys()):
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    conn.close()
                except OSError:
                    pass
            self._clients.clear()
        try:
            self._sock.close()
        except OSError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='멀티스레드 TCP 채팅 서버')
    parser.add_argument('--host', default='127.0.0.1', help='바인딩 호스트 (기본: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='포트 번호 (기본: 5000)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ChatServer(args.host, args.port)
    server.start()


if __name__ == '__main__':
    main()