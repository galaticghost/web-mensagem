import { useState } from "react";
import { registerUser } from "../service/authService"
import type { UserRegister } from "../types/types";
import { useNavigate } from "react-router";

export default function Register() {
    const [formData, setFormData] = useState<UserRegister>({
        username: "", email: "", password: "", password2: ""
    });

    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await registerUser(formData);
            setFormData({
                username: "", email: "", password: "", password2: ""
            });
            navigate("/auth/login");
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
            <label htmlFor="username">Username: </label>
            <input type="text" name="username" id="username"
                value={formData.username} onChange={handleChange} />

            <label htmlFor="email">Email: </label>
            <input type="email" name="email" id="email"
                value={formData.email} onChange={handleChange} />

            <label htmlFor="password">Password: </label>
            <input type="password" name="password" id="password"
                value={formData.password} onChange={handleChange} />

            <label htmlFor="password2">Confirm Password: </label>
            <input type="password" name="password2" id="password2"
                value={formData.password2} onChange={handleChange} />

            <button type="submit">Register</button>
        </form>
    )
}