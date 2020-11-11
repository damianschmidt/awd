import React, { useState } from "react";
import { Container } from "semantic-ui-react";
import HeaderBar from "./components/HeaderBar";
import DataForm from "./components/DataForm";
import InfoPanel from "./components/InfoPanel";

const App = () => {
  const [flightPlan, setFlightPlan] = useState({});

  return (
    <>
      <HeaderBar />
      <Container>
        <div className="main-body">
          <DataForm setFlightPlan={setFlightPlan} />
          <InfoPanel flightPlan={flightPlan} />
        </div>
      </Container>
    </>
  );
};

export default App;
