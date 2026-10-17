import { useState, useEffect } from 'react';

const API = "http://localhost:5555";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);	

  useEffect(() => {
    fetch(`${API}/check_session`, { credentials: "include" })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  },  []);

  if (loading) return <p>Checking...</p>;
  if (!user) return <p>Please log in</p>;
  return <h1>Welcome, {user.username}!</h1>;
}

export default App;
