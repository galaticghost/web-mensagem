import { useEffect, useState } from "react";
import { getMessageHistory } from "../../service/chatService";
import { websocket } from "../../websockets/socket";
import "../../styles/chatWindow.css";
import type { ReceivedMessage } from "../../types/types";
import { useAuth } from "../../hooks/useAuth";

interface ChatWindowProps {
    chatId: number | null;
}

export default function ChatWindow({ chatId }: ChatWindowProps) {
    const [message, setMessage] = useState<string>("")
    const [messages, setMessages] = useState<ReceivedMessage[]>([]);
    const { user } = useAuth();
    console.log(user?.id);
    useEffect(() => {
        loadHistory();
    }, [chatId]);

    const loadHistory = async () => {
        if (chatId === null) {
            return
        }
        const data = await getMessageHistory(chatId);
        console.log(data.messages);
        setMessages(data.messages);
    }

    useEffect(() => {
        websocket.onMessage((message) => {
            setMessages((prev) => [...prev, message]);
        })
    }, []);

    const handleMessageSend = async () => {
        if (chatId === null) {
            return;
        }

        await websocket.send({
            "message": message,
            "chatId": chatId
        });

        setMessage("");
    }

    const handleMessageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessage(e.target.value);
    }

    if (!chatId) {
        return (
            <section className="chat-window">
                <p>Teste</p>
            </section>
        )
    }

    return (
        <section className="chat-window">
            Chat selecionado: {chatId}
            <div className="message-div">
                {messages.map((msg) => (
                    <div key={msg.id} className={
                        `message ${msg.sender_id === user?.id ? "message-right" : "message-left"}`
                    }>
                        <p>{msg.message}</p>
                    </div>
                ))}
            </div>
            <input type="text" value={message} onChange={handleMessageChange} />
            <button onClick={handleMessageSend}>enviar</button>
        </section>
    )
}