import type { User } from "../../types/types";

interface UserItemProps {
    user: User;
    added: boolean;
    buttonText: string;
    handleAddUser: (id: number) => void | Promise<void>;
}

export default function UserItem({
    user,
    added,
    buttonText,
    handleAddUser
}: UserItemProps) {
    return (
        <li className={added ? "user user-added" : "user"}>
            <p>{user.username}</p>

            <button
                disabled={added}
                onClick={() => handleAddUser(user.id)}
            >
                {buttonText}
            </button>
        </li>
    );
}