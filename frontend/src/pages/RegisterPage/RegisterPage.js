import React, { useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import useCustomForm from "../../hooks/useCustomForm";

const RegisterPage = () => {
  const navigate = useNavigate();
  return (
    <div className="container">
      <button onClick={() => navigate("/normal-registration")}>Register as a persnal user</button>
      <button onClick={() => navigate("/student-registration")}>Register as a student</button>
      <button onClick={() => navigate("/teacher-registration")}>Register as a teacher</button>
    </div>
  );
};
//Button clues probably in navBar.jsx

export default RegisterPage;
