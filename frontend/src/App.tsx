import { registerUser } from "./service/loginService";

function App() {

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    registerUser(data);
  }

  return (
   <div>
    <p>japa</p>
    <form action="" onSubmit={handleSubmit}>
      <label htmlFor="username">Username: </label>
      <input type="text" name="username" id="username"/>
      <label htmlFor="email">Email: </label>
      <input type="email" name="email" id="email"/>
      <label htmlFor="password">Password: </label>
      <input type="password" name="password" id="password"/>
      <button type="submit">ssss</button>
    </form>
   </div>
  )
}

export default App
