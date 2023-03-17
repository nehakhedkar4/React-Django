import { useState, useEffect } from "react";
import axios from "axios";

const Fetchdata = () => {
    const [students, setStudent] = useState([]);
    useEffect(() => {
      async function fetchStudent() {
        try {
          const student = await axios.get("http://127.0.0.1:8000/");
          console.log(student.data);
          console.log("neha");
          setStudent(student.data);
        } catch (error) {
          console.log(error);
        }
      }
      fetchStudent();
    }, []);
    return (
      <>
        {" "}
        <div className="App">
          <h1>Hello!</h1>
          {students.map((s, i) => {
            return <h2>{s.name}</h2>;
          })}
        </div>
      </>
    );
  };

export default Fetchdata