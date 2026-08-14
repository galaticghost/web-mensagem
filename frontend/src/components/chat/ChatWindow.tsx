import React, { useEffect, useState, useRef, useLayoutEffect } from "react";
import { getMessageHistory } from "../../service/chatService";
import { websocket } from "../../websockets/socket";
import "../../styles/chatWindow.css";
import type { Chat, Message } from "../../types/types";
import { useAuth } from "../../hooks/useAuth";

interface ChatWindowProps {
    chat: Chat | null;
}

export default function ChatWindow({ chat }: ChatWindowProps) {
    const [message, setMessage] = useState<string>("")
    const [messages, setMessages] = useState<Message[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);
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

    useLayoutEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    useEffect(() => {
        websocket.onMessage((data) => {
            switch (data.type) {
                case "message":
                    const message = data.content;
                    if (message.chat_id === chat?.id) {
                        setMessages((prev) => [...prev, message]);
                    }
                    break
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

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            handleMessageSend()
        }
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
                <div ref={messagesEndRef} />
            </div>
            <div className="message-input">
                <input id="message" type="text" value={message} onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown} />
                <button onClick={handleMessageSend}>enviar</button>
            </div>

        </section>
    )
}