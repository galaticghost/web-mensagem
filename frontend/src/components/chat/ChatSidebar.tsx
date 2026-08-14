import { useEffect, useState } from "react"
import { getUserChats } from "../../service/chatService";
import "../../styles/chatSidebar.css";
import type { Chat } from "../../types/types";
import ChatHeader from "./ChatHeader";
import { websocket } from "../../websockets/socket";
import ChatFooter from "./ChatFooter";
import ChatItem from "./ChatItem";

interface ChatSidebarProps {
    setChat: (chat: Chat) => void;
    chatId: number | undefined;
}

export default function ChatSidebar({ setChat, chatId }: ChatSidebarProps) {
    const [chats, setChats] = useState<Chat[]>([]);
    const [search, setSearch] = useState<string>("");
    const [searchedChats, setSearchedChats] = useState<Chat[]>([]);

    const loadChats = async () => {
        const data = await getUserChats();
        setChats(data.chats);
    }

    useEffect(() => {
        if (chats && search) {
            const filterChats = chats.filter((chat) =>
                chat.display_name.toLowerCase().includes(search.toLowerCase())
            )
            setSearchedChats([...filterChats]);
        }
        if (search.length < 1) {
            setSearchedChats([]);
        }
    }, [search])

    useEffect(() => {
        loadChats();
    }, []);

    useEffect(() => {
        websocket.onNotification((data) => {
            switch (data.type) {
                case "new_chat":
                    setChats((prev) => [data.content, ...prev]);
                    break
                case "message":
                    setChats((prev) => {
                        const chat = prev.find(
                            (chat) => chat.id === data.content.chat_id
                        )

                        if (!chat) {
                            return prev;
                        }

                        return [
                            chat,
                            ...prev.filter(
                                (chat) => chat.id !== data.content.chat_id
                            )
                        ]
                    }
                    )
                    break
            }
        })
    }, [])

    return (
        <aside className="chat-sidebar">
            <ChatHeader
                search={search}
                setSearch={setSearch}
                chats={chats}
                loadChats={loadChats}
            />
            <section>
                <h1>Conversas</h1>
                <ul className="chat-list">
                    {searchedChats.length > 0 && chats ?
                        <>
                            {searchedChats.map((chat) => (
                                <ChatItem key={chat.id} chat={chat} setChat={setChat} />
                            ))}
                        </>
                        :
                        <>
                            {chats.map((chat) => (
                                <ChatItem key={chat.id} chat={chat} setChat={setChat} />
                            ))}
                        </>
                    }
                </ul>
            </section>
            <ChatFooter />
        </aside>
    )
}