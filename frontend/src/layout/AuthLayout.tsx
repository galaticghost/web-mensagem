import { Link, Outlet } from "react-router"

export default function AuthLayout() {
    return (
        <main>
            <div>
                <nav>
                    <Link to="/auth/login">Login</Link>
                    <Link to="/auth/register">Register</Link>
                </nav>
                <Outlet />
            </div>
        </main>
    )
}