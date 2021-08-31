import React from "react";
import { Container, Col, Row } from "reactstrap";
import Header from "../components/Header";
import {
	Card,
	Button,
	CardTitle,
	CardText,
	CardHeader,
	CardBody,
} from "reactstrap";

const ApiDoc = () => {
	return (
		<>
			<Header
				title='Api Documentation!'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utiility classes for typography and spacing to space
                content out within the larger container.'
			/>
			<Container fluid className='contant-container'>
				<Container
					style={{
						fontWeight: "bold",
						textAlign: "center",
						marginTop: "24px",
					}}>
					<Row>
						<Col>
							<Card>
								<CardHeader>
									<h3>API Documentation for AgriOracle</h3>
								</CardHeader>
								<CardBody>
									<CardTitle tag='h5'>Base URL</CardTitle>
									<CardText>https://agrioracle-rest.herokuapp.com/</CardText>
									<Button>Copy Clipboard</Button>
								</CardBody>
							</Card>
						</Col>
					</Row>
				</Container>
				<Container
					fulid
					style={{
						fontWeight: "bold",
						textAlign: "center",
						marginTop: "24px",
					}}>
					<Row style={{ margin: "25px" }}>
						<Col>
							<Card
								body
								inverse
								style={{
									backgroundColor: "#333",
									borderColor: "#333",
									height: "100%",
								}}>
								<CardTitle tag='h5'>End Point</CardTitle>
								<br />
								<br />
								<CardText>
									api/recommendation
									<br /> Methods = [GET , POST]
								</CardText>
								<br />
								<br />
								<Button>Copy Endpoint</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='primary'>
								<CardTitle tag='h5'>Parameters</CardTitle>
								<CardText>
									state - Required - String
									<br />
									city - Required - String
									<br />
									api_key - required - string
									<br />n - optional - int/float - <br /> p - optional -
									int/float -
									<br /> K - optional - int/float - <br /> Ph - optional -
									int/float - The PH value of Your soil <br />
								</CardText>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='success'>
								<CardTitle tag='h5'>Endpoint Response</CardTitle>
								<CardText style={{ height: "100%" }}>
									<br />
									<br />
									<code style={{ color: "white" }}>
										{
											"[{	‘Crop_name’ : predicted_crop	‘soilInfo’ : soil required for this crop	‘weatherInfo’ : suitable weather for this crop	‘Successchance’ : % value of success chance}]"
										}
									</code>
								</CardText>
								<Button>View Python Response</Button>
							</Card>
						</Col>
					</Row>
					<Row style={{ margin: "25px" }}>
						<Col>
							<Card
								body
								inverse
								style={{
									backgroundColor: "#333",
									borderColor: "#333",
									height: "100%",
								}}>
								<CardTitle tag='h5'>End Point</CardTitle>
								<br />
								<br />
								<CardText>
									api/yield
									<br /> Methods = [GET , POST]
								</CardText>
								<br />
								<br />
								<Button>Copy Endpoint</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='primary'>
								<CardTitle tag='h5'>Parameters</CardTitle>
								<CardText>
									state - Required - String
									<br />
									city - Required - String
									<br />
									api_key - required - string
									<br />
									season - required - string
									<br />
									crop - required - string
									<br />
									area - required - int/float
									<br />
								</CardText>
								<Button>View Details</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='success'>
								<CardTitle tag='h5'>Endpoint Response</CardTitle>
								<CardText style={{ height: "100%" }}>
									<br />
									<br />
									<code style={{ color: "white" }}>
										{
											"[   {        ‘predYield’ : expected yield in quintal/acre  ‘predProduction’ : predicted production in quintal    }     ]   "
										}
									</code>
								</CardText>
								<Button>View Python Response</Button>
							</Card>
						</Col>
					</Row>
					<Row style={{ margin: "25px" }}>
						<Col>
							<Card
								body
								inverse
								style={{
									backgroundColor: "#333",
									borderColor: "#333",
									height: "100%",
								}}>
								<CardTitle tag='h5'>End Point</CardTitle>
								<br />
								<br />
								<CardText>
									api/individual_price <br /> Methods = [GET , POST]
								</CardText>
								<br />
								<br />
								<Button>Copy Endpoint</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='primary'>
								<CardTitle tag='h5'>Parameters</CardTitle>
								<CardText>
									<br />
									api_key - required - string
									<br />
									crop_name - required - string - <br />
								</CardText>
								<br />
								<br />
								<Button>View Details</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='success'>
								<CardTitle tag='h5'>Endpoint Response</CardTitle>
								<CardText style={{ height: "100%" }}>
									<br />
									<br />
									<code style={{ color: "white" }}>
										{
											"                                            {                                                “Price”:                                                    [        {“month_name”: price}      ],            “Wpi” [             {“month_name”:wpi value}],“Change”:[ {“month_name”: change in demand}],   }            "
										}
									</code>
								</CardText>
								<Button>View Python Response</Button>
							</Card>
						</Col>
					</Row>
					<Row style={{ margin: "25px" }}>
						<Col>
							<Card
								body
								inverse
								style={{
									backgroundColor: "#333",
									borderColor: "#333",
									height: "100%",
								}}>
								<CardTitle tag='h5'>End Point</CardTitle>
								<br />
								<br />
								<CardText>
									api/top5
									<br /> Methods = [GET , POST]
								</CardText>
								<br />
								<br />
								<Button>Copy Endpoint</Button>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='primary'>
								<CardTitle tag='h5'>Parameters</CardTitle>
								<CardText>
									<br />
									api_key - required - string
									<br />
								</CardText>
							</Card>
						</Col>
						<Col>
							<Card style={{ height: "100%" }} body inverse color='success'>
								<CardTitle tag='h5'>Endpoint Response</CardTitle>
								<CardText style={{ height: "100%" }}>
									<br />
									<br />
									<code style={{ color: "white" }}>
										{
											"[{	‘Crop_name’ : predicted_crop	‘soilInfo’ : soil required for this crop	‘weatherInfo’ : suitable weather for this crop	‘Successchance’ : % value of success chance}]"
										}
									</code>
								</CardText>
								<Button>View Python Response</Button>
							</Card>
						</Col>
					</Row>
				</Container>
			</Container>
		</>
	);
};

export default ApiDoc;
