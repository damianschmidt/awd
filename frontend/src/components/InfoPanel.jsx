import React from "react";
import imageLogo from "../img/logo.png";
import { Divider, Grid, Header, Image, Segment } from "semantic-ui-react";
import Map from "./Map";

const InfoPanel = ({ flightPlan }) => {
  return (
    <Grid columns={2} stackable>
      <Grid.Column>
        <Segment>
          <Grid stackable columns={2}>
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
          </Grid>
        </Segment>
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
            <li>
              <p>
                Runway:&nbsp;&nbsp;{" "}
                {flightPlan[0]["runway ident"]
                  ? flightPlan[0]["runway ident"]
                  : "..."}{" "}
                {flightPlan[0]["runway surface"]
                  ? flightPlan[0]["runway surface"]
                  : "..."}{" "}
                13.123 x 148 ft ( 4.000 x 45 m )
              </p>
            </li>
          </ul>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
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
            <li>
              <p>
                Runway:&nbsp;&nbsp;{" "}
                {flightPlan[1]["runway ident"]
                  ? flightPlan[1]["runway ident"]
                  : "..."}{" "}
                {flightPlan[1]["runway surface"]
                  ? flightPlan[1]["runway surface"]
                  : "..."}{" "}
                13.123 x 148 ft ( 4.000 x 45 m )
              </p>
            </li>
          </ul>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
      </Grid.Column>
      <Grid.Column>
        <Segment>
          <Map flightPlan={flightPlan} />
        </Segment>
      </Grid.Column>
    </Grid>
  );
};

export default InfoPanel;
