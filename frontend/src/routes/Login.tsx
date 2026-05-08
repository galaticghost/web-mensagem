import { useState } from "react";
import { loginUser } from "../service/authService"
import type { UserLogin } from "../types/types";
import { useNavigate } from "react-router";

export default function Login() {
    const [formData, setFormData] = useState<UserLogin>({
        email: "", password: ""
    });

    const navigate = useNavigate();

    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await loginUser(formData);
            setFormData({
                email: "", password: ""
            });
            navigate("/chat");
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error(error.message);
            }
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email: </label>
            <input type="email" name="email" id="email"
                value={formData.email} onChange={handleChange} />

            <label htmlFor="password">Password: </label>
            <input type="password" name="password" id="password"
                value={formData.password} onChange={handleChange} />

            <button type="submit">Login</button>
        </form>
    )
}