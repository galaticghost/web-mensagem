import { useState } from "react";
import ChatSidebar from "../components/chat/ChatSidebar"
import ChatWindow from "../components/chat/ChatWindow"
import '../styles/chat.css';
import type { Chat } from "../types/types";

export default function Chat() {
    const [selectedChat, setSelectedChat] = useState<Chat | null>(null);

    return (

        <main className="chat">
            <ChatSidebar
                onSelectChat={setSelectedChat}
            />
            <ChatWindow
                chat={selectedChat}
            />
        </main>
    )
}