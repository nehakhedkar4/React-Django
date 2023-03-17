import { Route, Routes } from "react-router-dom";
import Fetchdata from "./components/Fetchdata";

function App() {
  return (
    <>
      <Routes>
        <Route path="/fetchdata" element={ <Fetchdata /> }  />
      </Routes>
    </>
  );
}

export default App;
