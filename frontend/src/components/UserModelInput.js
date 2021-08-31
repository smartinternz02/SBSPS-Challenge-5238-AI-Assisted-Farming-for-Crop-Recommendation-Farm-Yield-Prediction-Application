import React, { useState, useEffect } from "react";
import {
	Container,
	Row,
	Col,
	Button,
	CardTitle,
	Card,
	CardText,
	FormGroup,
	Label,
	Input,
} from "reactstrap";
import { Form, ProgressBar } from "react-bootstrap";
import Toggle from "react-toggle";
import "./css/ToggleSwitch.scss";
import SeasonName from "../jsondropdown/season_name_for_yield.json";
import firstletterCap from "../utills/firstletterCap";
import ReactApexChart from "react-apexcharts";
import API from "../utills/Api";

const UserModelInput = (props) => {
	const [isChecked, setisChecked] = useState(true);
	const [apiResult, setApiResult] = useState(false);
	const [findYieldShow, setfindYieldShow] = useState(false);
	const [yieldResult, setyieldResult] = useState(false);
	const [YieldCrops, setYieldCrop] = useState([]);
	const [Phosphoras, setPhosphoras] = useState("");
	const [Potassium, setPotassium] = useState("");
	const [Ph, setPh] = useState("");
	const [displayInput, setdisplayInput] = useState(false);
	const [SelectedSeason, setSelectedSeason] = useState("");
	const [Nitrogen, setNitrogen] = useState("");
	const [area, setarea] = useState(0);
	const [SelectedCropYield, setSelectedCropYield] = useState("");
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
	const toggalSwitch = () => {
		let curCheck = !isChecked;
		if (curCheck) {
			setdisplayInput(false);
			setPhosphoras(getRandomInt(10, 100));
			setPotassium(getRandomInt(10, 100));
			setNitrogen(getRandomInt(10, 100));
			setPh(getRandomInt(0.5, 13));
			console.log(Ph);
		} else {
			setdisplayInput(true);
			setPhosphoras(0);
			setPotassium(0);
			setNitrogen(0);
			setPh(0);
			console.log(Ph);
		}
		setisChecked(curCheck);
	};

	const callCropPersonalApi = async () => {
		const data = {
			model_name: props.ModelName,
			ph: Ph,
			n: Nitrogen,
			p: Phosphoras,
			k: Potassium,
		};
		await API.post(
			"/user_recommendation_model",
			{ ...data },
			{
				headers: {
					"x-access-tokens": localStorage.getItem("jwt"),
				},
			}
		)
			.then((res) => {
				console.log({ ...res.data });
				let res_data = { ...res.data };
				let cropArr = [];
				let top5 = res.data.Top5CropInfo;
				for (let i = 0; i < 5; i++) {
					console.log(top5[i].cropName);
					cropArr.push(top5[i].cropName);
				}
				setYieldCrop(cropArr);
				console.log(YieldCrops);

				setApiResult(res_data);
			})
			.catch((err) => {
				console.log(err);
			});
	};
	const callYieldPersonalApi = async () => {
		const data = {
			model_name: props.ModelName,
			season: SelectedSeason,
			crop: SelectedCropYield,
			area: area,
		};
		console.log(data);
		await API.post(
			"/user_yield_model",
			{ ...data },
			{
				headers: {
					"x-access-tokens": localStorage.getItem("jwt"),
				},
			}
		)
			.then((res) => {
				const res_data = { ...res.data };
				console.log(res_data);
				setyieldResult(res_data);
			})
			.catch((err) => {
				console.log(err);
			});
	};
	return (
		<>
			<Container>
				<Row>
					<Col style={{ textAlign: "center", margin: "25px" }}>
						<h3 style={{ fontWeight: "bold", marginLeft: "20px" }}>
							{props.ModelName} Model
						</h3>
					</Col>
				</Row>
				<Container>
					<Row style={{ textAlign: "left" }}>
						<Col xs={5} style={{ textAlign: "right", margin: "3px" }}>
							<Toggle
								defaultChecked={isChecked}
								className='custom-classname'
								onChange={() => toggalSwitch()}
							/>
						</Col>
						<Col>
							<h4>Automate Your Response</h4>
						</Col>
					</Row>
				</Container>
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
								placeholder='Potatiam'
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
				<Row>
					<Col style={{ textAlign: "center", marginTop: "24px" }}>
						<Button
							onClick={(e) => {
								e.preventDefault();
								callCropPersonalApi();
							}}>
							Get Results
						</Button>
					</Col>
				</Row>
			</Container>

			{apiResult ? (
				<>
					<Container fluid style={{ margin: "24px" }}>
						<Container style={{ margin: "24px auto 24px auto" }}>
							<Row>
								{apiResult.Top5CropInfo.map((crop, idx) => {
									return (
										<Col key={idx}>
											<Card body>
												<CardTitle
													style={{ fontSize: "24px", fontWeight: "bold" }}
													tag='h5'>
													{firstletterCap(crop.cropName)}
												</CardTitle>
												<CardText>
													<ProgressBar
														now={crop.successChance}
														label={`${crop.successChance}%`}
														style={{ marginBottom: "20px", marginTop: "20px" }}
													/>
												</CardText>
											</Card>
										</Col>
									);
								})}
							</Row>
						</Container>
						<Row>
							<Col style={{ textAlign: "center" }}>
								<h3 style={{ margin: "50px" }}>Pi Chart of Success</h3>
								<Button
									color='primary'
									onClick={(e) => {
										e.preventDefault();
										setfindYieldShow(true);
									}}>
									Find Yield
								</Button>
							</Col>
							<Col>
								<ReactApexChart
									options={{
										chart: {
											width: 500,
											type: "pie",
										},
										labels:
											apiResult.static_info.pieChartOfSuccessPercentageLabel,
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
										apiResult.static_info.pieChartOfSuccessPercentageValue
									}
									type='pie'
									width={500}
								/>
							</Col>
						</Row>
					</Container>
					{findYieldShow ? (
						<Container className='contant-container'>
							<Row>
								<Col style={{ textAlign: "center" }}>
									<h3 style={{ fontWeight: "bold" }}>Find Yield</h3>
								</Col>
							</Row>
							<Row style={{ padding: "25px", marginTop: "24px" }}>
								<Col xs={3}>
									<Label>Model Name</Label>

									<Form.Control
										style={{ marginTop: "48px" }}
										value={props.ModelName}
										placeholder='Model Name'
									/>
								</Col>
								<Col xs={3}>
									<FormGroup>
										<Label>Season</Label>
										<Input
											type='select'
											name='season'
											value={SelectedSeason}
											onChange={(e) => setSelectedSeason(e.target.value)}
											style={{ marginTop: "47px" }}>
											<option selected value>
												-- select an option --
											</option>

											{SeasonName.season.map((season, idx) => {
												return (
													<option key={idx} value={season}>
														{firstletterCap(season)}
													</option>
												);
											})}
										</Input>
									</FormGroup>{" "}
								</Col>
								<Col xs={3}>
									<FormGroup>
										<Label>Crop</Label>
										<Input
											type='select'
											name='crop'
											defaultValue={"none"}
											value={SelectedCropYield}
											onChange={(e) => setSelectedCropYield(e.target.value)}
											style={{ marginTop: "47px" }}>
											<option selected value>
												-- select an option --
											</option>
											{YieldCrops.map((crop, idx) => {
												return (
													<option key={idx} value={crop}>
														{firstletterCap(crop)}
													</option>
												);
											})}
										</Input>
									</FormGroup>
								</Col>
								<Col xs={3}>
									<Label>Area</Label>

									<Form.Control
										style={{ marginTop: "48px" }}
										value={area}
										onChange={(e) => setarea(e.target.value)}
										placeholder='Area'
									/>
								</Col>
							</Row>
							<Row>
								<Col style={{ textAlign: "center", marginTop: "12px" }}>
									<Button
										onClick={(e) => {
											e.preventDefault();
											callYieldPersonalApi();
										}}>
										Get Yield Results
									</Button>
								</Col>
							</Row>
						</Container>
					) : null}
					{yieldResult ? (
						<Container>
							<Row>
								<Col>
									<Card
										body
										inverse
										style={{ backgroundColor: "#333", borderColor: "#333" }}>
										<CardTitle tag='h5'>Predicted Yield</CardTitle>
										<CardText>{yieldResult.predProduction} / Quintal</CardText>
									</Card>
								</Col>
								<Col>
									<Card
										body
										inverse
										style={{ backgroundColor: "#333", borderColor: "#333" }}>
										<CardTitle tag='h5'>Predicted Production</CardTitle>
										<CardText>
											{yieldResult.predYield} / Quintal/Hectare
										</CardText>
									</Card>
								</Col>
							</Row>
						</Container>
					) : null}
				</>
			) : null}
		</>
	);
};

export default UserModelInput;
