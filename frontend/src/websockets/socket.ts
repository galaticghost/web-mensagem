import { refresh } from "../service/authService";
import type { SendMessage, ReceivedMessage } from "../types/types";

class WebSocketService {
    private websocket: WebSocket | null = null
    private accessToken: string | null = null;
    private messageCallback?: (msg: ReceivedMessage) => void;

    connect(access_token: string) {
        this.accessToken = access_token;
        const url = `ws://127.0.0.1:8000/ws/user?token=${access_token}`;

        if (this.websocket) {
            return;
        }

        this.websocket = new WebSocket(url);

        this.websocket.onopen = () => {
            console.log("Websocket conectado");
        }

        this.websocket.onclose = async (ev: CloseEvent) => {
            console.log("Websocket desconectado");
            this.websocket = null
            console.log(ev.reason)
            if (ev.reason === "TOKEN_EXPIRED") {
                await this.reconnect();
                return
            }
            setTimeout(() => {
                if (this.accessToken) {
                    this.connect(this.accessToken);
                }
            }, 3000);
        }

        this.websocket.onerror = (error) => {
            console.error("Erro no websocket", error);
        };

        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case "message":
                    console.log(data);
                    this.messageCallback?.(data);
                    break;
            }
        }

    }

    async reconnect() {
        const refreshToken = localStorage.getItem("refresh_token");
        try {
            if (refreshToken === null) {
                throw new Error("NO_REFRESH_TOKEN");
            }

            const tokens = await refresh(refreshToken);

            localStorage.setItem("access_token", tokens.access_token);
            localStorage.setItem("refresh_token", tokens.refresh_token);
            localStorage.setItem("token_type", tokens.token_type);

            this.connect(tokens.access_token);
            return
        } catch {
            localStorage.clear();
            window.location.href = "/auth/login"; // mudar para router TODO
        }
    }

    disconnect() {
        this.accessToken = null;
        this.websocket?.close();
        this.websocket = null;
    }

    sendMessage(data: SendMessage) {
        if (!this.websocket) {
            throw new Error("WebSocket não conectado");
        }

        this.websocket.send(JSON.stringify({
            "type": "message",
            "content": {
                "message": data.message,
                "chat_id": data.chatId
            }

        }))
    }

    onMessage(callback: (msg: ReceivedMessage) => void) {
        this.messageCallback = callback;
    }
}

export const websocket = new WebSocketService();