import React from "react";
import { Container } from "semantic-ui-react";
import HeaderBar from "./components/HeaderBar";
import DataForm from "./components/DataForm";
import InfoPanel from "./components/InfoPanel";

const App = () => {
  return (
    <>
      <HeaderBar />
      <Container>
        <div className="main-body">
          <DataForm />
          <InfoPanel />
        </div>
      </Container>
    </>
  );
};

export default App;
