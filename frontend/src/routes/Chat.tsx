import ChatSidebar from "../components/chat/ChatSidebar"
import ChatWindow from "../components/chat/ChatWindow"
import '../styles/chat.css';

export default function Chat() {


    return (
        <main className="chat">
            <ChatSidebar />
            <ChatWindow />
        </main>
    )
}