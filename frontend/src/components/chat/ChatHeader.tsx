import SearchChatBar from "./SearchChatBar";
import { useAuth } from "../../hooks/useAuth";

interface ChatHeaderProps {
    search: string;
    setSearch: (value: string) => void;
}

export default function ChatHeader({search,setSearch}: ChatHeaderProps) {
    const { logout } = useAuth();
    
    return (
        <section>
            <section>            
                <h2>Web-Mensagens</h2>
                <button>AddChat</button>
                <button onClick={logout}>Logout</button>
            </section>
            <SearchChatBar
                search={search}
                setSearch={setSearch}
            />
        </section>
    )
}