import { registerUser, loginUser } from "./service/loginService";

function App() {

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    registerUser(data);
  }

  const handleLogin = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    loginUser(data);
  }

  return (
    <div>
      <p>japa</p>
      <form action="" onSubmit={handleSubmit}>
        <label htmlFor="username">Username: </label>
        <input type="text" name="username" id="username" />
        <label htmlFor="email">Email: </label>
        <input type="email" name="email" id="email" />
        <label htmlFor="password">Password: </label>
        <input type="password" name="password" id="password" />
        <label htmlFor="password2">Confirm Password: </label>
        <input type="password" name="password2" id="password2" />
        <button type="submit">ssss</button>
      </form>

      <form onSubmit={handleLogin}>
        <label htmlFor="email">Email: </label>
        <input type="email" name="email" id="email" />
        <label htmlFor="password">Password: </label>
        <input type="password" name="password" id="password" />
        <button type="submit">ssss</button>
      </form>
    </div>
  )
}

export default App
