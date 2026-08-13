import { useAuth } from "../../hooks/useAuth";

export default function ChatFooter () {
    const { logout } = useAuth();
    
    return <section className="chat-footer">
        <button>Config</button>
        <button>ToggleTheme</button>
        <button onClick={logout}>Logout</button>
    </section>
}