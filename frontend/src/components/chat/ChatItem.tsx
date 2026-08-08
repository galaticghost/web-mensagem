import type {User} from "../../types/types";

interface ChatItemProps {
    handleAddUser: (id: number) => void;
    user: User;
}

export default function ChatItem({user,handleAddUser}: ChatItemProps) {
    return (
        <li key={user.id}>
            <p>{user.username}</p>
            <button onClick={() => handleAddUser(user.id)}>Add</button>
        </li>
    )
}