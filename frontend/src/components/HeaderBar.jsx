import React from "react";
import { Container, Header, Image, Menu } from "semantic-ui-react";
import image from "../img/logo.png";

const HeaderBar = () => {
  return (
    <Menu>
      <Container>
        <Menu.Item as="a" header>
          <Image size="mini" src={image} style={{ marginRight: "1.5em" }} />
          AWD
        </Menu.Item>
        <Header as="h2"></Header>
      </Container>
    </Menu>
  );
};

export default HeaderBar;
