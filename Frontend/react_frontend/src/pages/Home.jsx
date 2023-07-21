import AdminPanel from "../components/AdminPanel/AdminPanel";
import { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";
import { decodeToken } from "react-jwt";
import './Home.css'
import Navbar from "../components/Navbar";
import Dashboard from "../components/Dashboard/Dashboard";

const Home = () => {
   const { store } = useContext(Context)
   const [current_username, setCurrent_username] = useState("")
   const [current_user, setCurrent_user] = useState([])
   const [isAdminView, setIsAdminView] = useState("")
   const [toggle, setToggle] = useState(false)

   useEffect(() => {
      const getRole = () => {
         if (store.token && store.token !== undefined && store.token !== null) {
            const myDecodedToken = decodeToken(store.token);
            const current = myDecodedToken.current_user
            sessionStorage.setItem("current_User", JSON.stringify(current))
            const checkrole = myDecodedToken.is_administrator
            setCurrent_user(current)
            setCurrent_username(current.username)
            setIsAdminView(checkrole)
            sessionStorage.setItem("current_user", current)
         }
      }
      getRole()
   }, [store.token]);

   return (
      <div className=" bg-slate-600">
         <Navbar isAdminView={isAdminView}/>
         <Dashboard />
         {(isAdminView) ?
            <h1><AdminPanel /></h1> :
            <h1>{current_username} is not admin</h1>}
      </div>

   )
}

export default Home;