import React from "react";
import { Container, Row, Col, Jumbotron, Button } from "react-bootstrap";
import "./css/Header.css";
import NavBar from "./NavBar";
const Header = (props) => {
	return (
		<>
			<Container fluid className='header-img'>
				<Row>
					<Col>
						<NavBar></NavBar>
					</Col>
				</Row>
				<Row>
					<Col>
						<Jumbotron fluid className='jumbotron-container'>
							<h1 className='display-3'>{props.title}</h1>
							{/* <p className='lead'>{props.desc1}</p> */}
							<hr className='my-2' />
							{/* <p>{props.desc2}</p> */}
							<p className='lead'>
								{/* <Button color='primary'>Learn More</Button> */}
							</p>
						</Jumbotron>
					</Col>
				</Row>
			</Container>
		</>
	);
};

export default Header;
