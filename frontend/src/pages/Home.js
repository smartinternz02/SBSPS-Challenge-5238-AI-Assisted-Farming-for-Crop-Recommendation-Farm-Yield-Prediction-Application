import React from "react";
import Header from "../components/Header";
import { Container, Col, Row } from "reactstrap";
import "./css/Home.css";
import HomeCards from "../components/HomeCards";
const Home = () => {
	return (
		<>
			<Header
				title='A Tool For Future!'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'></Header>
			<Container fluid className='contant-container'>
				<Row className='heading-container'>
					<Col className='heading-text-container'>
						<h1 className='heading-text'>About Us</h1>
					</Col>
				</Row>
			</Container>

			<Container fluid className='contant-container'>
				<Row className=''>
					<Col>
						<HomeCards aboutus={true}></HomeCards>
					</Col>
				</Row>
			</Container>

			<Container fluid className='contant-container'>
				<Row className='heading-container'>
					<Col className='heading-text-container'>
						<h1 className='heading-text'>Tools We Offer</h1>
					</Col>
				</Row>
			</Container>
			<Container fluid className='contant-container'>
				<Row className=''>
					<Col>
						<HomeCards tools={true}></HomeCards>
					</Col>
				</Row>
			</Container>
		</>
	);
};

export default Home;
