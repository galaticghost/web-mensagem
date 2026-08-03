import { useState } from "react";
import ChatSidebar from "../components/chat/ChatSidebar"
import ChatWindow from "../components/chat/ChatWindow"
import '../styles/chat.css';

export default function Chat() {
    const [selectedChat, setSelectedChat] = useState<number | null>(null);

    return (
        <main className="chat">
            <ChatSidebar
                onSelectChat={setSelectedChat}
            />
            <ChatWindow
                chatId={selectedChat}
            />
        </main>
    )
}