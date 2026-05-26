import "./index.css";
import { useState } from "react";

export default function App() {

  const [page,setPage] = useState("home");

  return (

    <div className="app">

      <div className="top-bar">
        <h2>3D Assistant AI</h2>

        <div className="top-icons">
          <span>🔔</span>
          <span>⚙️</span>
        </div>
      </div>

      {page === "home" && (

        <>
          <div className="hero-card">

            <div className="hero-text">
              <h1>Premium+</h1>
              <p>AI powered Telegram Mini App</p>
            </div>

            <div className="hero-badge">
              💎 PRO
            </div>

          </div>

          <div className="stats">

            <div className="stat-card">
              <h2>24K</h2>
              <p>Users</p>
            </div>

            <div className="stat-card">
              <h2>$89K</h2>
              <p>Revenue</p>
            </div>

          </div>
        </>
      )}

      {page === "premium" && (

        <>
          <div className="section-title">
            Premium Plans
          </div>

          <div className="plan-card active-plan">

            <div className="plan-top">
              <span>🔥 1 Oylik Obuna</span>
            </div>

            <h1>34.999 so'm</h1>

            <div className="card-box">

  <div className="card-item">
    💳 Visa
  </div>

  <div className="card-item">
    🟣 Uzcard
  </div>

  <div className="card-item">
    🔵 Humo
  </div>

</div>

<button className="buy-btn">
  Obuna Bo'lish
</button>

          </div>

          <div className="plan-card">

            <div className="plan-top">
              <span>💎 3 Oylik Premium</span>
            </div>

            <h1>95.000 so'm</h1>

            <div className="card-box">

  <div className="card-item">
    💳 Visa
  </div>

  <div className="card-item">
    🟣 Uzcard
  </div>

  <div className="card-item">
    🔵 Humo
  </div>

</div>

<button className="buy-btn">
  Obuna Bo'lish
</button>

          </div>
        </>
      )}

      {page === "profile" && (

        <>
          <div className="profile-card">

            <div className="avatar">
              😎
            </div>

            <h2>Akram</h2>

            <p>Premium User</p>

          </div>

          <div className="stats">

            <div className="stat-card">
              <h2>145</h2>
              <p>Projects</p>
            </div>

            <div className="stat-card">
              <h2>5⭐</h2>
              <p>Rating</p>
            </div>

          </div>
        </>
      )}

      <div className="bottom-nav">

        <button
          className={`nav-btn ${page==="home" ? "active" : ""}`}
          onClick={()=>setPage("home")}
        >
          <span>🏠</span>
          <p>Asosiy</p>
        </button>

        <button
          className={`nav-btn ${page==="premium" ? "active" : ""}`}
          onClick={()=>setPage("premium")}
        >
          <span>💎</span>
          <p>Obuna</p>
        </button>

        <button
          className={`nav-btn ${page==="profile" ? "active" : ""}`}
          onClick={()=>setPage("profile")}
        >
          <span>👤</span>
          <p>Profil</p>
        </button>

      </div>

    </div>
  );
}