import React from "react";
import imageMap from "../img/map.png";
import { Divider, Grid, Header, Image, Segment } from "semantic-ui-react";

const InfoPanel = () => {
  return (
    <Grid columns={2}>
      <Grid.Column>
        <Segment>
          <Grid columns={2}>
            <Divider vertical>
              {/* <Image src={image} size="mini" /> */}
            </Divider>
            <Grid.Column textAlign="center">
              <Header as="h4">Rio Galeao</Header>
              <p>SBGL</p>
              <p>Gate 533</p>
            </Grid.Column>
            <Grid.Column textAlign="center">
              <Header as="h4">Presidente Juscelino</Header>
              <p>SBBR</p>
            </Grid.Column>
          </Grid>
        </Segment>
        <Segment>
          <Header as="h4">Departure Info</Header>
          <p>Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010</p>
          <p>Runway: 10 CON 13.123 x 148 ft ( 4.000 x 45 m )</p>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
        <Segment>
          <Header as="h4">Arrival Info</Header>
          <p>Weather: SBGL 092000Z 29002KT 9999 FEW020 BKN100 25/22 Q1010</p>
          <p>Runway: 11L ASP 10.499 x 148 ft ( 3.200 x 45 m ) lighted</p>
          <p>.</p>
          <p>.</p>
          <p>.</p>
        </Segment>
      </Grid.Column>
      <Grid.Column>
        <Image fluid src={imageMap} />
      </Grid.Column>
    </Grid>
  );
};

export default InfoPanel;
