import { useCallback, useEffect, useState } from "react"
import { searchUsers } from "../../service/userService";
import { createPrivateChat, getUserChats } from "../../service/chatService";
import { debounce } from "../../utils/utils"
import "../../styles/chatSidebar.css";
import type { User, Chat } from "../../types/types";
import ChatItem from "./ChatItem";
import ChatHeader from "./ChatHeader";

interface ChatSidebarProps {
    onSelectChat: (id: number) => void;
}

export default function ChatSidebar({ onSelectChat }: ChatSidebarProps) {
    const [username, setUsername] = useState<string>("");
    const [searchedUsers, setSearchedUsers] = useState<User[] | null>(null);
    const [chats, setChats] = useState<Chat[] | null>(null);
    const [search, setSearch] = useState<string>("");

    const loadChats = async () => {
        const data = await getUserChats();
        setChats(data.chats);
    }

    useEffect(() => {
        if (chats && search) {
            const filterChats = chats.filter((chat) => 
                chat.display_name.toLowerCase().includes(search.toLowerCase())
            )
            console.log(filterChats)
        }
    },[search])

    useEffect(() => {
        loadChats();
    }, []);

    useEffect(() => {
       if (username.length < 3) { 
            setSearchedUsers([]); 
            return; 
        }
        handleSearch(username);
    },[username])

    const handleSearch = useCallback(
        debounce(async (value: string) => {
            try {
                if (value.length < 3){
                    return;
                } 
                const users = await searchUsers(value);
                setSearchedUsers(users); 
            } catch (error: unknown) { 
                if (error instanceof Error) { 
                    console.error(error.message); 
                } 
            }
        }),
        []
    );  

    const handleAddUser = async (id: number) => {
        await createPrivateChat(id);
        setUsername("");
        setSearchedUsers(null);
        await loadChats();
    }

    return (
        <aside className="chat-sidebar">
            <ChatHeader
                search={search}
                setSearch={setSearch}
            />
            <section>
                <label htmlFor="add">Adicione alguem</label>
                <input type="text" name="add" value={username}
                    onChange={(e) => setUsername(e.target.value)} />
                {searchedUsers &&
                    <ul>
                        {searchedUsers.map((user) => (
                            <ChatItem
                            user={user}
                            handleAddUser={handleAddUser}
                            />
                        ))}
                    </ul>
                }
            </section>
            <section>
                {chats &&
                    <ul>
                        {chats.map((chat) => (
                            <li key={chat.id}>
                                <button onClick={() => onSelectChat(chat.id)}>
                                    <p>{chat.display_name}</p>
                                </button>
                            </li>
                        ))}
                    </ul>
                }
            </section>
        </aside>
    )
}