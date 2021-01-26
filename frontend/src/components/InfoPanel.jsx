import React, { useEffect, useState } from "react";
import imageLogo from "../img/logo.png";
import { Divider, Grid, Header, Image, Segment } from "semantic-ui-react";
import Map from "./Map";
import axios from "axios";
import AproachDetails from "./aproachDetails";

const InfoPanel = ({ flightPlan, dateTime }) => {
  const [loading, setLoading] = useState(false);
  const [weather, setWeather] = useState({
    dep: {
      windSpeed: "...",
      windDirection: "...",
      pressure: "...",
      precipitation: "...",
      temp: "...",
    },
    arr: {
      windSpeed: "...",
      windDirection: "...",
      pressure: "...",
      precipitation: "...",
      temp: "...",
    },
  });

  useEffect(() => {
    if (flightPlan[0]) {
      (async () => {
        setLoading(true);
        const res = [];
        res.push(
          JSON.parse(
            "[" +
              (
                await axios.get(
                  `http://127.0.0.1:5000/api/weather/${flightPlan[0].icao}/${dateTime[0]}`
                )
              ).data +
              "]"
          )
        );

        res.push(
          JSON.parse(
            "[" +
              (
                await axios.get(
                  `http://127.0.0.1:5000/api/weather/${flightPlan[1].icao}/${dateTime[0]}`
                )
              ).data +
              "]"
          )
        );

        setWeather({
          dep: {
            windSpeed: parseInt(parseFloat(res[0][0][0]) * 1.94384449),
            windDirection: res[0][0][5],
            pressure: parseInt(res[0][0][2]),
            precipitation: parseInt(res[0][0][3]),
            temp: parseInt(res[0][0][4]),
          },
          arr: {
            windSpeed: parseInt(parseFloat(res[1][0][0]) * 1.94384449),
            windDirection: res[1][0][5],
            pressure: parseInt(res[1][0][2]),
            precipitation: parseInt(res[1][0][3]),
            temp: parseInt(res[1][0][4]),
          },
        });

        setLoading(false);
      })();
    }
  }, [flightPlan[0]]);

  return (
    <Grid columns={2} stackable>
      <Grid.Row stretched>
        <Grid.Column>
          <Segment className="routePointToPoint">
            <Grid stackable columns={2}>
              <Grid.Row>
                <Divider vertical>
                  <Image src={imageLogo} size="mini" />
                </Divider>
                <Grid.Column textAlign="center">
                  <Header as="h4">
                    {flightPlan[0].name ? flightPlan[0].name : "..."}
                  </Header>
                  <p>{flightPlan[0].icao ? flightPlan[0].icao : "..."}</p>
                </Grid.Column>
                <Grid.Column textAlign="center">
                  <Header as="h4">
                    {flightPlan[1].name ? flightPlan[1].name : "..."}
                  </Header>
                  <p>{flightPlan[1].icao ? flightPlan[1].icao : "..."}</p>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <Grid.Column>
                  <p>
                    Date:&nbsp;&nbsp;{dateTime[0] ? dateTime[0] : "..."}
                    &nbsp;&nbsp;/&nbsp;&nbsp;{dateTime[1]
                      ? dateTime[1]
                      : "..."}{" "}
                  </p>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Segment>
          <Segment>
            <AproachDetails {...{ weather, loading, flightPlan }} />
          </Segment>
        </Grid.Column>
        <Grid.Column>
          <Segment>
            <Map flightPlan={flightPlan} />
          </Segment>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column>
          <Segment>
            <Header as="h4">Departure Info</Header>
            <p>
              Name:&nbsp;&nbsp;{flightPlan[0].name ? flightPlan[0].name : "..."}
              &nbsp; ({flightPlan[0].icao ? flightPlan[0].icao : "..."})
            </p>
            <p>
              Elevation:&nbsp;&nbsp;
              {parseInt(
                flightPlan[0].elevation ? flightPlan[0].elevation : "..."
              )}
              &nbsp;ft
            </p>
            <p>Runways:</p>
            <ul>
              {flightPlan[0]["runway ident"]
                ? flightPlan[0]["runway ident"].map((runway, i) => (
                    <li key={i}>
                      <p>
                        Runway:&nbsp;&nbsp; {runway ? runway : "..."}
                        &nbsp;&nbsp;
                        {flightPlan[0]["runway surface"][i]
                          ? flightPlan[0]["runway surface"][i]
                          : "..."}
                        &nbsp;&nbsp;
                        {flightPlan[0]["runway length"][i]
                          ? parseInt(flightPlan[0]["runway length"][i])
                          : "..."}{" "}
                        ft
                      </p>
                    </li>
                  ))
                : ""}
            </ul>
            <p>
              Weather:&nbsp;&nbsp;{weather.dep.windSpeed}kt&nbsp;&nbsp;
              {weather.dep.windDirection}&nbsp;&nbsp;{weather.dep.precipitation}
              mm&nbsp;&nbsp;{weather.dep.pressure}hPa&nbsp;&nbsp;
              {weather.dep.temp}°C
            </p>
          </Segment>
        </Grid.Column>
        <Grid.Column>
          <Segment>
            <Header as="h4">Arrival Info</Header>
            <p>
              Name:&nbsp;&nbsp;{flightPlan[1].name ? flightPlan[1].name : "..."}
              &nbsp; ({flightPlan[0].icao ? flightPlan[0].icao : "..."})
            </p>
            <p>
              Elevation:&nbsp;&nbsp;
              {parseInt(
                flightPlan[0].elevation ? flightPlan[0].elevation : "..."
              )}
              &nbsp;ft
            </p>
            <p>Runways:</p>
            <ul>
              {flightPlan[1]["runway ident"]
                ? flightPlan[1]["runway ident"].map((runway, i) => (
                    <li key={i}>
                      <p>
                        Runway:&nbsp;&nbsp; {runway ? runway : "..."}
                        &nbsp;&nbsp;
                        {flightPlan[1]["runway surface"][i]
                          ? flightPlan[1]["runway surface"][i]
                          : "..."}
                        &nbsp;&nbsp;
                        {flightPlan[1]["runway length"][i]
                          ? parseInt(flightPlan[1]["runway length"][i])
                          : "..."}{" "}
                        ft
                      </p>
                    </li>
                  ))
                : ""}
            </ul>
            <p>
              Weather: &nbsp;&nbsp;{weather.arr.windSpeed}kt&nbsp;&nbsp;
              {weather.arr.windDirection}&nbsp;&nbsp;{weather.arr.precipitation}
              mm&nbsp;&nbsp;{weather.arr.pressure}hPa&nbsp;&nbsp;
              {weather.arr.temp}°C
            </p>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

export default InfoPanel;
