import React, { useState } from "react";
import {
	Container,
	Col,
	Row,
	Button,
	FormGroup,
	Label,
	Input,
} from "reactstrap";
import { Form, Card, Table } from "react-bootstrap";
import Header from "../components/Header";
import "./css/PriceFinder.css";
import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import ArrowDropUpIcon from "@material-ui/icons/ArrowDropUp";
import TrendingFlatIcon from "@material-ui/icons/TrendingFlat";
import ReactApexChart from "react-apexcharts";
import API from "../utills/Api";
import CropPriceDownOption from "../jsondropdown/croprice.json";
import capitalizeFirstLetter from "../utills/firstletterCap";

const PriceFinder = () => {
	const [showResult, setShowResult] = useState(false);
	const [SelectedCrop, setSelectedCrop] = useState("");
	const [result, setresult] = useState();

	const ButtonshowResult = async () => {
		const data = {
			crop_name: SelectedCrop,
		};
		console.log(SelectedCrop);
		await API.post("/individual_price", { ...data })
			.then((res) => {
				const res_data = { ...res.data };
				console.log(res_data);
				setresult(res_data);
				setShowResult(true);
			})
			.catch((err) => {
				console.log(err);
			});
	};
	return (
		<>
			<Header
				title='Find The Real Price!'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'
			/>
			<Container fluid className='contant-container'>
				<Row>
					<Col className='heading-text-container'>
						<h1 style={{ fontSize: "48px" }}>Price Finder</h1>
					</Col>
				</Row>
			</Container>
			<Container fluid className='contant-container'>
				<Container style={{ margin: "auto", padding: "10px" }}>
					<Row>
						<Col>
							<Form>
								<Row style={{ justifyContent: "center" }}>
									<Col xs={3}>
										<FormGroup>
											<Label for='exampleSelect'>Crop Name</Label>
											<Input
												type='select'
												name='state'
												onChange={(e) => setSelectedCrop(e.target.value)}
												style={{ marginTop: "24px" }}>
												{CropPriceDownOption.cropName.map((cName, idx) => {
													return (
														<option key={idx} value={cName}>
															{capitalizeFirstLetter(cName)}
														</option>
													);
												})}
											</Input>
										</FormGroup>
									</Col>
									<Col xs={3}>
										<Button
											style={{ width: "100px", marginTop: "46px" }}
											color='primary'
											onClick={(e) => {
												e.preventDefault();
												ButtonshowResult();
											}}>
											Submit
										</Button>
									</Col>
								</Row>
							</Form>
						</Col>
					</Row>
				</Container>
			</Container>
			{showResult ? (
				<Container fluid className='contant-container'>
					<Row style={{ margin: "auto", padding: "25px" }}>
						<Col xs={2} style={{ margin: "auto" }}>
							<Card.Title style={{ fontSize: "48px", paddingBottom: "25px" }}>
								{capitalizeFirstLetter(result.cropName)}
							</Card.Title>
						</Col>
						<Col xs={5}>
							<Table style={{ textAlign: "center" }} bordered hover>
								<tbody>
									<tr>
										<td>Base Price 2020 </td>
										<td>{result.basePrice2020}</td>
									</tr>
									<tr>
										<td>Base Price 2021</td>
										<td>{result.basePrice2021}</td>
									</tr>
									<tr>
										<td>Export Country</td>
										<td>{result.exportCountry}</td>
									</tr>
									<tr>
										<td>Production States</td>
										<td>{result.productionState}</td>
									</tr>
									<tr>
										<td>Production Season</td>
										<td>{result.productionSeason}</td>
									</tr>
								</tbody>
							</Table>
						</Col>
						<Col xs={3}>
							<Card.Img
								variant='top'
								src={`/crop_price_img/${result.imageUrl}`}
							/>
						</Col>
					</Row>
				</Container>
			) : (
				<Container fluid className='contant-container centerHowTo'>
					<Row>
						<Container>
							<Row>
								<Col>
									<div class='description'>
										<h1 className='PriceFinderText'>How To Use</h1>

										<p>
											Crop price is the service of the team agrioracle in which
											user get the forecast of price for upto 12 months by just
											selecting the crops. <br />
											we had predicted the price based on the demand and supply
											month wise. We had also compared the price of previous
											year so user can get the idea what to do. <br />
											if user is able to find the possible price month wise he
											can get the maximum profit by selling its crops at right
											time
										</p>
									</div>
								</Col>
							</Row>
						</Container>
					</Row>
				</Container>
			)}
			{showResult ? (
				<>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<h2 style={{ textAlign: "center", fontSize: "48px" }}>
									Past Price and Wholesale Index Price
								</h2>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "line",
											zoom: {
												enabled: false,
											},
										},
										dataLabels: {
											enabled: false,
										},
										stroke: {
											curve: "straight",
										},
										title: {
											text: "Previous Price Trend by Month",
											align: "center",
										},
										grid: {
											row: {
												colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
												opacity: 0.5,
											},
										},
										xaxis: {
											categories: result.forGraphPreviousX,
										},
									}}
									series={[
										{
											name: "Previous Price ",
											data: result.forGraphPreviousYPrice,
										},
									]}
									type='line'
									height={350}
								/>
							</Col>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "line",
											zoom: {
												enabled: false,
											},
										},
										dataLabels: {
											enabled: false,
										},
										stroke: {
											curve: "straight",
										},
										title: {
											text: "Wholesale Index Price Trend by Month",
											align: "center",
										},
										grid: {
											row: {
												colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
												opacity: 0.5,
											},
										},
										xaxis: {
											categories: result.forGraphPreviousX,
										},
									}}
									series={[
										{
											name: "Wholesale Index Price ",
											data: result.forGraphPreviousYWpi,
										},
									]}
									type='line'
									height={350}
								/>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<h2 style={{ textAlign: "center", fontSize: "48px" }}>
									Price and Wholesale Index Price Forcast
								</h2>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "line",
											zoom: {
												enabled: false,
											},
										},
										dataLabels: {
											enabled: false,
										},
										stroke: {
											curve: "straight",
										},
										title: {
											text: "Price Trend Forcast by Month",
											align: "center",
										},
										grid: {
											row: {
												colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
												opacity: 0.5,
											},
										},
										xaxis: {
											categories: result.forGraphForecastX,
										},
									}}
									series={[
										{
											name: "Price Forcast ",
											data: result.forGraphForecastYPrice,
										},
									]}
									type='line'
									height={350}
								/>
							</Col>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "line",
											zoom: {
												enabled: false,
											},
										},
										dataLabels: {
											enabled: false,
										},
										stroke: {
											curve: "straight",
										},
										title: {
											text: "Wholesale Index Price Trend Forcast by Month",
											align: "center",
										},
										grid: {
											row: {
												colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
												opacity: 0.5,
											},
										},
										xaxis: {
											categories: result.forGraphForecastX,
										},
									}}
									series={[
										{
											name: "Wholesale Index Price ",
											data: result.forGraphForecastYWpi,
										},
									]}
									type='line'
									height={350}
								/>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col style={{ textAlign: "left" }}>
								<h3 style={{ fontSize: "30px", fontWeight: "bold" }}>
									Price Forcast
								</h3>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<Table striped bordered hover>
									<thead>
										<tr>
											<th>Date</th>
											<th>Price</th>
											<th>WIP</th>
											<th>Change</th>
										</tr>
									</thead>

									<tbody>
										{result.priceForecast.map((item, idx) => {
											const upordown = (i) => {
												if (i > 0) {
													return (
														<td>
															<ArrowDropUpIcon style={{ color: "green" }} />
															{i}
														</td>
													);
												}
												if (i < 0) {
													return (
														<td>
															<ArrowDropDownIcon style={{ color: "red" }} />
															{i}
														</td>
													);
												} else {
													return (
														<td>
															<TrendingFlatIcon style={{ color: "green" }} />
															{i}
														</td>
													);
												}
											};
											return (
												<tr>
													<td>{item[0]}</td>
													<td>{item[1]}</td>
													<td>{item[2]}</td>
													{upordown(item[3])}{" "}
												</tr>
											);
										})}
									</tbody>
								</Table>
							</Col>
						</Row>
					</Container>
				</>
			) : null}
		</>
	);
};

export default PriceFinder;
