import type { SendMessage, ReceivedMessage } from "../types/types";

class WebSocketService {
    private websocket: WebSocket | null = null
    private accessToken: string | null = null;

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

        this.websocket.onclose = () => {
            console.log("Websocket desconectado");
            this.websocket = null
            setTimeout(() => {
                if (this.accessToken) {
                    this.connect(this.accessToken);
                }
            }, 3000);
        }

        this.websocket.onerror = (error) => {
            console.error("Erro no websocket", error);
        };
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
                "type":"message",
                "content":{
                    "message": data.message,
                    "chat_id": data.chatId
                }
        
        }))
    }

    sendToken() {
        if (!this.websocket) {
            throw new Error("WebSocket não conectado");
        }
        const refreshToken = localStorage.getItem("refresh_token");

        this.websocket.send(JSON.stringify({
                "type":"refresh",
                "content":{
                    "refresh_token": refreshToken
                }
            })
        )
    }

    onMessage(callback: (data: ReceivedMessage) => void) {
        if (!this.websocket) {
            //Isso daqui meio que quebra e não permite a reconexão
            //throw new Error("WebSocket não conectado");
            return
        }
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            callback(data);
        };
    }
}

export const websocket = new WebSocketService();