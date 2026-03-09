import { useState } from 'react'
import './App.css'

function App() {
  const [username, setUserName] = useState("")
  const [password, setPassword] = useState("")
  const [mode, setMode] = useState("secure")
  const [result, setResult] = useState<any>(null)

  async function submitForm() {
    const url = "http://localhost:8000/login/" + mode

    const response = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json" },
      body: JSON.stringify({username, password})
    })

    const data = await response.json()

    setResult(data)
  }

  return (
    <div>
      <h1> SQL Injection Demo (Educational purposes only)</h1>
      <form onSubmit={(e) => { e.preventDefault();submitForm(); }}> 
        <div>
          <label>Username</label>
          <input type="text" value={username} placeholder="Enter username" onChange={(e) => setUserName(e.target.value)}/>
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} placeholder="Enter password" onChange={(e) => setPassword(e.target.value)}/>
        </div>
        <button name="submit">Login</button>
      <div>
        <button onClick={() => setMode(mode == "secure" ? "vulnerable" : "secure")}>
          Mode: {mode}
        </button>
      </div>
      </form>

       {result && (
      <div>
        <p> Query: {result.query || result.param_query} </p>
        <p> Results: {JSON.stringify(result.results)}</p>
      </div>
    )}
    </div>
  )

    
}

export default App
