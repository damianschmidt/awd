import React, { useEffect, useState } from "react";
import { Header, Loader } from "semantic-ui-react";

const AproachDetails = ({ weather, loading, flightPlan }) => {
  const [runway, setRunway] = useState("");
  const [ice, setIce] = useState("");
  const [baro, setBaro] = useState("");
  const [ab, setAb] = useState("4");

  const azymut = (str) => {
    switch (str) {
      case "N":
        return 0;

      case "NE":
        return 45;

      case "E":
        return 90;

      case "SE":
        return 135;

      case "S":
        return 180;

      case "SW":
        return 225;

      case "W":
        return 270;

      case "NW":
        return 315;

      default:
        return 0;
    }
  };

  useEffect(() => {
    const wind = azymut(weather.arr.windDirection);
    let smallest = 360;
    let index = 0;

    if (flightPlan[1]) {
      flightPlan[1]["runway ident"].forEach((e, i) => {
        const diff = Math.abs(e - wind / 10);
        if (diff < smallest) {
          smallest = diff;
          setRunway(e);
          index = i;
        }
      });

      weather.arr.temp <= 10 ? setIce("ON") : setIce("OFF");
      setBaro(weather.arr.pressure);

      if (flightPlan[1]["runway length"][index] > 10000) setAb(1);
      if (flightPlan[1]["runway length"][index] > 9000) {
        setAb(2);
      } else if (flightPlan[1]["runway length"][index] < 9000) {
        if (weather.arr.precipitation < 5) {
          setAb(2);
        } else if (weather.arr.precipitation < 10) {
          setAb(3);
        } else {
          setAb(4);
        }
      }

      if (flightPlan[1]["runway length"][index] < 6000) {
        if (weather.arr.precipitation < 5) {
          setAb(3);
        } else {
          setAb(4);
        }
      }
    }
  }, [flightPlan[1], weather.arr.pressure]);

  return (
    <>
      <div className="form-btn">
        <div>
          <Header as="h4">APPROACH DETAILS</Header>
          <p>Runway:&nbsp;&nbsp;{runway}</p>
          <p>Anti-Ice:&nbsp;&nbsp;{ice} </p>
          <p>Auto break:&nbsp;&nbsp;{ab} </p>
          <p>Baro:&nbsp;&nbsp;{baro} hPa</p>
        </div>
        {loading ? <Loader active inline /> : <Loader disabled inline />}
      </div>
    </>
  );
};

export default AproachDetails;
