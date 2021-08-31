import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import {
	Container,
	Col,
	Row,
	Button,
	FormGroup,
	Label,
	Input,
} from "reactstrap";
import { Form, Card, ProgressBar } from "react-bootstrap";
import CapFirst from "../utills/firstletterCap";
import ReactApexChart from "react-apexcharts";
import Toggle from "react-toggle";
import "../components/css/ToggleSwitch.scss";
import API from "../utills/Api";
import cityState from "../jsondropdown/city_state_name.json";

const CropRecomendation = () => {
	const [isChecked, setisChecked] = useState(true);
	const [Phosphoras, setPhosphoras] = useState("");
	const [Potassium, setPotassium] = useState("");
	const [Ph, setPh] = useState("");
	const [Nitrogen, setNitrogen] = useState("");
	const [displayInput, setdisplayInput] = useState(false);
	const [city, setCity] = useState("");
	const [State, setState] = useState("gujarat");
	const [cropRecommendationData, setcropRecommendationData] = useState({});
	const [shownCrop, setshownCrop] = useState(false);
	const [showGrid, setshowGrid] = useState(false);
	const [Loading, setLoading] = useState(false);

	const getCity = (stateName) => {
		let cities = cityState[stateName];
		console.log(cities);
		return cities.map((city, idx) => {
			return (
				<option key={idx} value={city}>
					{CapFirst(city)}
				</option>
			);
		});
	};
	const states = () => {
		var keys = Object.keys(cityState);
		return keys.map((state, idx) => {
			return (
				<option key={idx} value={state}>
					{CapFirst(state)}
				</option>
			);
		});
	};

	function getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	useEffect(() => {
		setPhosphoras(getRandomInt(10, 100));
		setPotassium(getRandomInt(10, 100));
		setNitrogen(getRandomInt(10, 100));
		setPh(getRandomInt(0.5, 13));
	}, []);

	const handleShow = (crop) => {
		setshownCrop(crop);
	};
	const formSubbmit = async () => {
		console.log(Ph, Nitrogen, Phosphoras, Potassium);
		const data = {
			state: "gujarat",
			city: "ahmedabad",
			ph: Ph,
			n: Nitrogen,
			p: Phosphoras,
			k: Potassium,
		};
		setLoading(true);
		await API.post("/recommendation", { ...data })
			.then((res) => {
				const data = res.data;
				console.log(res.data);
				setcropRecommendationData(data);
				setLoading(false);
			})
			.catch((err) => {
				setLoading(false);

				console.log(err);
			});
		setshowGrid(true);
	};
	const toggalSwitch = () => {
		let curCheck = !isChecked;
		if (curCheck) {
			setPhosphoras(0);
			setPotassium(0);
			setNitrogen(0);
			setPh(0);
			console.log(Ph);
			setdisplayInput(false);
		} else {
			setPhosphoras(getRandomInt(10, 100));
			setPotassium(getRandomInt(10, 100));
			setNitrogen(getRandomInt(10, 100));
			setPh(getRandomInt(0.5, 13));
			console.log(Ph);
			setdisplayInput(true);
		}
		setisChecked(curCheck);
	};
	return (
		<>
			<Header
				title='A Tool For Future!'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'
			/>

			<Container fluid className='contant-container'>
				<Row style={{ margin: "auto", textAlign: "center" }}>
					<Col
						style={{
							margin: "24px",
							textAlign: "center",
						}}>
						<h3 style={{ fontSize: "48px" }}>Crop Recomendation</h3>
					</Col>
				</Row>
			</Container>
			<Container fluid className='contant-container'>
				<Row>
					<Col>
						<Container>
							<Form>
								<Row style={{ marginTop: "24px", marginBottom: "24px" }}>
									<Col xs={5}>
										<FormGroup>
											<Label>State</Label>
											<Input
												type='select'
												name='State'
												value={State}
												onChange={(e) => setState(e.target.value)}
												style={{ marginTop: "24px" }}>
												<option selected value>
													-- select an option --
												</option>
												{states()}
											</Input>
										</FormGroup>
									</Col>
									<Col xs={5}>
										<FormGroup>
											<Label>City</Label>
											<Input
												type='select'
												name='city'
												onChange={(e) => setCity(e.target.value)}
												value={city}
												style={{ marginTop: "24px" }}>
												<option selected value>
													-- select an option --
												</option>
												{getCity(State)}
											</Input>
										</FormGroup>
									</Col>
								</Row>
								{Loading ? (
									<Container fluid className='content-container'>
										<Row>
											<Col>
												<h3>Loading...</h3>
											</Col>
										</Row>
									</Container>
								) : null}
								{displayInput ? (
									<Row style={{ padding: "25px", marginTop: "24px" }}>
										<Col xs={3}>
											<Form.Control
												value={Ph}
												onChange={(e) => setPh(e.target.value)}
												placeholder='PH'
											/>
										</Col>
										<Col xs={3}>
											<Form.Control
												value={Potassium}
												onChange={(e) => setPotassium(e.target.value)}
												placeholder='Potassium'
											/>
										</Col>
										<Col xs={3}>
											<Form.Control
												value={Phosphoras}
												onChange={(e) => setPhosphoras(e.target.value)}
												placeholder='Phosphoras'
											/>
										</Col>
										<Col xs={3}>
											<Form.Control
												value={Nitrogen}
												onChange={(e) => setNitrogen(e.target.value)}
												placeholder='Nitrogen'
											/>
										</Col>
									</Row>
								) : null}
								<Row style={{ marginTop: "24px", marginBottom: "24px" }}>
									<Col style={{ padding: "25px", textAlign: "right" }}>
										<Toggle
											defaultChecked={isChecked}
											className='custom-classname'
											onChange={() => toggalSwitch()}
										/>
									</Col>
									<Col>
										<h4 style={{ marginTop: "20px" }}>
											Automate Your Response
										</h4>
									</Col>
									<Col style={{ padding: "20px", textAlign: "left" }}>
										<Button onClick={() => formSubbmit()} color='primary'>
											Submit
										</Button>
									</Col>
								</Row>
							</Form>
						</Container>
					</Col>
				</Row>
			</Container>
			{showGrid ? (
				<>
					<Container fluid className='contant-container'>
						<Row>
							<Col
								style={{
									textAlign: "center",
									padding: "25px",
								}}>
								<h2 style={{ fontWeight: "bold", fontSize: "40px" }}>
									Predicted Crops
								</h2>
							</Col>
						</Row>
					</Container>

					<Container fluid className='contant-container'>
						<Row>
							{cropRecommendationData.Top5CropInfo.map((crop, idx) => {
								return (
									<>
										<Col key={idx}>
											<Card
												style={{
													width: "18rem",
													margin: "auto",
													marginTop: "50px",
												}}>
												<Card.Img
													variant='top'
													src={`/crop_image/${crop.imagePath}`}
												/>
												<Card.Body>
													<Card.Title>
														{CapFirst(crop.productionName)}
													</Card.Title>
													<Card.Text
														style={{ fontWeight: "bold", textAlign: "center" }}>
														Success Chances
													</Card.Text>
													<ProgressBar
														now={crop.successChance}
														label={`${crop.successChance}%`}
														style={{ marginBottom: "20px", marginRight: "0px" }}
													/>
													<Button
														variant='primary'
														key={idx}
														className='me-2'
														onClick={() => handleShow(crop)}>
														Get Info
													</Button>
												</Card.Body>
											</Card>
										</Col>
									</>
								);
							})}
						</Row>
					</Container>
				</>
			) : (
				<Container fluid className='contant-container'>
					<Container className='contant-container centerHowTo'>
						<Row>
							<Col>
								<div class='description'>
									<h1 className='PriceFinderText'>How To Use</h1>
									<h2 className='PriceFinderText-Secondary'>
										Opening a door to the future
									</h2>
									<p style={{ fontSize: "24px" }}>
										Crop recommendation is the service of agrioracle in which
										user can get max 5 predicted crops based on weather and soil
										parameters. Just by selecting the location user can get
										predicted crops and its analysis. <br /> For Soil parameters
										we have two option either select Our Iot service or Manually
										define the values. We will return the top 5 predicted crops
										and its success chance and the analysis of the weather and
										soil.
									</p>
								</div>
							</Col>
						</Row>
					</Container>
				</Container>
			)}

			{showGrid ? (
				<Container fluid className='contant-container'>
					<Row>
						<Col xs={3} style={{ margin: "auto" }}>
							<h2 style={{ fontWeight: "bold" }}>Pi Chart of Success</h2>
						</Col>
						<Col xs={2} style={{ margin: "auto" }}>
							<ReactApexChart
								options={{
									chart: {
										width: 500,
										type: "pie",
									},
									labels:
										cropRecommendationData.static_info
											.pieChartOfSuccessPercentageLabel,
									responsive: [
										{
											breakpoint: 480,
											options: {
												chart: {
													width: 300,
												},
												legend: {
													position: "bottom",
												},
											},
										},
									],
								}}
								series={
									cropRecommendationData.static_info
										.pieChartOfSuccessPercentageValue
								}
								type='pie'
								width={500}
							/>
						</Col>
					</Row>
				</Container>
			) : null}

			{shownCrop ? (
				<>
					<Container fluid className='contant-container'>
						<Row>
							<Col style={{ textAlign: "center", padding: "25px" }}>
								<h1>{CapFirst(shownCrop.productionName)}</h1>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col style={{ textAlign: "left", padding: "25px" }}>
								<h1>Soil Information</h1>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											type: "bar",
											height: 430,
										},
										title: {
											text: "Soil Analysis",
										},
										plotOptions: {
											bar: {
												horizontal: false,
												dataLabels: {
													position: "top",
												},
											},
										},
										dataLabels: {
											enabled: true,
											offsetX: -6,
											style: {
												fontSize: "12px",
												colors: ["#fff"],
											},
										},
										stroke: {
											show: true,
											width: 1,
											colors: ["#fff"],
										},
										tooltip: {
											shared: true,
											intersect: false,
										},
										xaxis: {
											categories:
												cropRecommendationData.static_info.soilBarChartLabel,
										},
									}}
									series={[
										{ name: "Required Soil", data: shownCrop.soilInfo },
										{
											name: "Your Soil",
											data: cropRecommendationData.static_info
												.soilBarChartUserValue,
										},
									]}
									type='bar'
									height={500}
								/>
							</Col>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "radar",
											dropShadow: {
												enabled: true,
												blur: 1,
												left: 1,
												top: 1,
											},
										},
										title: {
											text: "Radar Chart - Multi Series",
										},
										stroke: {
											width: 2,
										},
										fill: {
											opacity: 0.1,
										},
										markers: {
											size: 0,
										},
										xaxis: {
											categories:
												cropRecommendationData.static_info.soilBarChartLabel,
										},
									}}
									series={[
										{ name: "Required Soil", data: shownCrop.soilInfo },
										{
											name: "Your Soil",
											data: cropRecommendationData.static_info
												.soilBarChartUserValue,
										},
									]}
									type='radar'
									height={500}
								/>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col style={{ textAlign: "left", padding: "25px" }}>
								<h1>Weather Information</h1>
							</Col>
						</Row>
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											type: "bar",
											height: 430,
										},
										title: {
											text: "Soil Analysis",
										},
										plotOptions: {
											bar: {
												horizontal: false,
												dataLabels: {
													position: "top",
												},
											},
										},
										dataLabels: {
											enabled: true,
											offsetX: -6,
											style: {
												fontSize: "12px",
												colors: ["#fff"],
											},
										},
										stroke: {
											show: true,
											width: 1,
											colors: ["#fff"],
										},
										tooltip: {
											shared: true,
											intersect: false,
										},
										xaxis: {
											categories:
												cropRecommendationData.static_info.weatherBarChartLabel,
										},
									}}
									series={[
										{ name: "Required Weather", data: shownCrop.weatherInfo },
										{
											name: "Your Weather",
											data: cropRecommendationData.static_info
												.weatherBarChartUserValue,
										},
									]}
									type='bar'
									height={500}
								/>
							</Col>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											height: 350,
											type: "radar",
											dropShadow: {
												enabled: true,
												blur: 1,
												left: 1,
												top: 1,
											},
										},
										title: {
											text: "Radar Chart - Multi Series",
										},
										stroke: {
											width: 2,
										},
										fill: {
											opacity: 0.1,
										},
										markers: {
											size: 0,
										},
										xaxis: {
											categories:
												cropRecommendationData.static_info.weatherBarChartLabel,
										},
									}}
									series={[
										{ name: "Required Weather", data: shownCrop.weatherInfo },
										{
											name: "Your Weather",
											data: cropRecommendationData.static_info
												.weatherBarChartUserValue,
										},
									]}
									type='radar'
									height={500}
								/>
							</Col>
						</Row>
					</Container>
				</>
			) : null}
		</>
	);
};

export default CropRecomendation;
