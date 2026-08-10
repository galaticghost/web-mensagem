import { useEffect, useState } from "react";
import { getMessageHistory } from "../../service/chatService";
import { websocket } from "../../websockets/socket";
import "../../styles/chatWindow.css";
import type { Chat, ReceivedMessage } from "../../types/types";
import { useAuth } from "../../hooks/useAuth";

interface ChatWindowProps {
    chat: Chat | null;
}

export default function ChatWindow({ chat }: ChatWindowProps) {
    const [message, setMessage] = useState<string>("")
    const [messages, setMessages] = useState<ReceivedMessage[]>([]);
    const { user } = useAuth();

    useEffect(() => {
        setMessages([]);
        if (chat === null) {
            return
        }

        const loadHistory = async () => {
            const data = await getMessageHistory(chat.id);
            setMessages(data.messages);
        }
        loadHistory();
    }, [chat]);

    useEffect(() => {
        websocket.onMessage((message) => {
            if (message.chat_id === chat?.id) {
                setMessages((prev) => [...prev, message]);
            }
        })
    }, [chat]);

    const handleMessageSend = () => {
        if (chat === null || message === "") {
            return;
        }

        websocket.sendMessage({
            "message": message,
            "chatId": chat.id
        });

        setMessage("");
    }

    if (!chat?.id) {
        return (
            <section className="chat-window">
                <p>Nenhum chat selecionado</p>
            </section>
        )
    }

    return (
        <section className="chat-window">
            Chat selecionado: {chat.id}
            <div className="message-div">
                {messages.map((msg) => (
                    <div key={msg.id} className={
                        `message 
                        ${msg.sender_id === user?.id ? "message-right" : "message-left"} 
                        ${chat.type === "group" ? "group-message" : "private-message"}`
                    }>
                        <p>{msg.message}</p>
                    </div>
                ))}
            </div>
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
            <button onClick={handleMessageSend}>enviar</button>
        </section>
    )
}