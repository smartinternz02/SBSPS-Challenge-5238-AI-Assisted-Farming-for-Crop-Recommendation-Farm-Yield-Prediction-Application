import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import firstletterCap from "../utills/firstletterCap";
import { Redirect } from "react-router-dom";
import examplecsv from "../jsondropdown/personal_model.csv";
import {
	Container,
	Col,
	Row,
	Card,
	CardHeader,
	CardBody,
	Collapse,
	CardTitle,
	CardText,
} from "reactstrap";
import API from "../utills/Api";
import { Table, Button } from "react-bootstrap";
import "./css/TrainModel.css";
import UserModelInput from "../components/UserModelInput";
const TrainModel = () => {
	const [Modelname, setModelname] = useState("");
	const [cityName, setCityName] = useState("");
	const [stateName, setStateName] = useState("");
	const [useModel, setUseModel] = useState("");
	const [SelectedFile, setSelectedFile] = useState(false);
	const [toggleQuestion, setToggequestion] = useState(1);
	const [isRedirect, setisRedirect] = useState(false);
	const [isAuth, setisAuth] = useState();
	const [ModelNames, setModelNames] = useState([]);
	const [isLoading, setisLoading] = useState(true);
	const [isError, setisError] = useState(false);
	const [errorMessage, setErrorMessage] = useState("");
	const [isSuccess, setisSuccess] = useState(false);
	const [trainLoad, setTrainLoad] = useState(false);
	const [SuccessMessage, setSuccessMessage] = useState("");
	useEffect(() => {
		async function checkLogin() {
			let response = await API.get("/check", {
				headers: {
					"x-access-tokens": localStorage.getItem("jwt"),
				},
			});
			response = await response;
			let res_data = { ...response.data };
			console.log(res_data);
			if (res_data.isAuthenticated) {
				setisLoading(false);
				setisAuth(true);
			} else {
				setisLoading(false);
				setisRedirect(true);
			}
		}
		checkLogin();
	}, []);
	useEffect(() => {
		async function getTrainedModels() {
			let response = await API.get("/user_models", {
				headers: {
					"x-access-tokens": localStorage.getItem("jwt"),
				},
			});
			response = await response;
			let res_data = response.data.names;
			setModelNames(res_data);
		}
		getTrainedModels();
	}, [isAuth]);

	const onSubmit = async (e) => {
		e.preventDefault();
		const form = new FormData();
		console.log(SelectedFile);
		form.append("csvfile", SelectedFile, "csvfile");
		form.append("model_name", Modelname);
		form.append("city_name", cityName);
		form.append("state", stateName);
		setTrainLoad(true);
		await API.post("/personal_model", form, {
			headers: {
				"Content-Type": "multipart/form-data,",
				"x-access-tokens": localStorage.getItem("jwt"),
			},
		})
			.then((res) => {
				const res_data = { ...res.data };
				if (!res_data.result) {
					setTrainLoad(false);

					setErrorMessage(res_data.message);
					setisError(true);
				} else {
					setTrainLoad(false);

					setSuccessMessage(
						res_data.messgae + "Please Refresh to Use Your Model"
					);
					setisSuccess(true);
				}
			})
			.catch((err) => {
				console.log(err);
			});
	};

	return (
		<>
			<Header
				title='Train Your Own Model'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'
			/>

			{isLoading ? (
				<Container fluid className='contant-container'>
					<Row>
						<Col>
							<h3 style={{ textAlign: "center" }}>
								Checking Authentication.....
							</h3>
						</Col>
					</Row>
				</Container>
			) : null}

			{isAuth ? (
				<>
					<Container fluid className='contant-container'>
						<Container fluid>
							<Row>
								<Col>
									<Card className='train-cards-collapse'>
										<CardHeader
											style={{ textAlign: "center" }}
											onClick={() => setToggequestion(1)}>
											<span style={{ fontSize: "40px" }}>How To Use</span>
										</CardHeader>
										<Collapse isOpen={toggleQuestion === 1 ? true : false}>
											<CardBody
												style={{
													width: "100%",
													height: "20%",
													textAlign: "center",
												}}>
												<p>
													For further accuracy Improvements we had given the
													option of prediction for specific data for the
													authenticated user.User can train his/her personal
													model and get its prediction.User have to upload csv
													file in the given format. <br /> Csv file limitation:
													It must be less than 15 mb. <br />
													It should contains the 12 columns and all the 12
													columns should be in order. The value of each column
													has to be valid other wise model training is not
													possible. The user should upload valid csv file.
												</p>
												<a
													style={{ textDecoration: "none" }}
													href={examplecsv}
													download='example.csv'>
													<Button>Download Example CSV File</Button>{" "}
												</a>
											</CardBody>
										</Collapse>
									</Card>

									<Card className='train-cards-collapse'>
										<CardHeader
											style={{ textAlign: "center" }}
											onClick={() => setToggequestion(2)}>
											<span style={{ fontSize: "40px" }}>
												Train A New Model
											</span>
										</CardHeader>
										<Collapse isOpen={toggleQuestion === 2 ? true : false}>
											<CardBody>
												<Container>
													<form>
														<div class='form-group'>
															<label for='exampleInputEmail1'>
																Name Your Model
															</label>
															<input
																class='form-control'
																placeholder='Model Name'
																type='text'
																value={Modelname}
																onChange={(e) => setModelname(e.target.value)}
															/>
														</div>
														<div class='form-group'>
															<label for='exampleInputEmail1'>City</label>
															<input
																class='form-control'
																placeholder='City (Spelling and Case Sensitive)'
																type='text'
																value={cityName}
																onChange={(e) => setCityName(e.target.value)}
															/>
														</div>
														<div class='form-group'>
															<label for='exampleInputEmail1'>State</label>
															<input
																class='form-control'
																placeholder='State (Spelling and Case Sensitive)'
																type='text'
																value={stateName}
																onChange={(e) => setStateName(e.target.value)}
															/>
														</div>
														<div class='form-group'>
															<label for='csvupload'>Upload CSV</label>
															<input
																class='form-control'
																placeholder='Upload FIle'
																type='file'
																name='CSV'
																onChange={(e) =>
																	setSelectedFile(e.target.files[0])
																}
															/>
														</div>
														<button
															type='submit'
															onClick={(e) => onSubmit(e)}
															class='btn btn-primary'>
															Submit
														</button>
													</form>
												</Container>
											</CardBody>
										</Collapse>
									</Card>
								</Col>
							</Row>
						</Container>
					</Container>
					<Container className='contant-conatiner'>
						{trainLoad ? (
							<Container fluid className='contant-container'>
								<Row>
									<Col>
										<h3 style={{ textAlign: "center" }}>Loading Results</h3>
									</Col>
								</Row>
							</Container>
						) : null}
						{isError ? (
							<Card body inverse color='danger'>
								<CardTitle tag='h5'>Error</CardTitle>
								<CardText>{errorMessage}</CardText>
							</Card>
						) : null}
						{isSuccess ? (
							<Card body inverse color='success'>
								<CardTitle tag='h5'>Success</CardTitle>
								<CardText>{SuccessMessage}</CardText>
							</Card>
						) : null}
					</Container>
					<Container fluid className='contant-container'>
						<Row>
							<Col>
								<Card className='train-cards-collapse'>
									<CardHeader
										style={{ textAlign: "center" }}
										onClick={() => setToggequestion(3)}>
										<span style={{ fontSize: "40px" }}>
											Your Trained Models
										</span>
									</CardHeader>
									<Container>
										<Row>
											<Col>
												<CardBody>
													<Table striped bordered hover>
														<thead>
															<tr>
																<th>#</th>
																<th>Model Name</th>
																<th>Use Model</th>
															</tr>
														</thead>
														<tbody>
															{ModelNames.map((nmx, idx) => {
																console.log(ModelNames);
																console.log(nmx);
																return (
																	<tr>
																		<td>{idx + 1}</td>
																		<td>{firstletterCap(nmx)}</td>
																		<td>
																			<Button
																				onClick={(e) => {
																					e.preventDefault();
																					setUseModel(nmx);
																				}}
																				color='primary'>
																				Use {firstletterCap(nmx)} Model
																			</Button>
																		</td>
																	</tr>
																);
															})}
														</tbody>
													</Table>
												</CardBody>
											</Col>
										</Row>
									</Container>
								</Card>
							</Col>
						</Row>
					</Container>
					{useModel ? (
						<Container fluid className='contant-container'>
							<Row>
								<Col>
									<UserModelInput ModelName={useModel} />
								</Col>
							</Row>
						</Container>
					) : null}
				</>
			) : null}
			{isRedirect ? <Redirect to='/auth' /> : null}
		</>
	);
};

export default TrainModel;
