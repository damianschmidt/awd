import React from "react";
import imageLogo from "../img/logo.png";
import { Divider, Grid, Header, Image, Segment } from "semantic-ui-react";
import Map from "./Map";

const InfoPanel = ({ flightPlan, dateTime }) => {
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
            <Header as="h4">APPROACH DETAILS</Header>
            <p>Runway: </p>
            <p>Anti-Ice: </p>
            <p>Flight Level: </p>
            <p>Baro: </p>
            <p>Auto break: </p>
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
            <p>Weather: ...</p>
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
            <p>Weather: ...</p>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

export default InfoPanel;
