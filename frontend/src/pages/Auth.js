import React, { useState, useEffect } from "react";
import {
	Container,
	Col,
	Row,
	Button,
	Card,
	CardBody,
	CardTitle,
	CardText,
} from "reactstrap";
import Header from "../components/Header";
import API from "../utills/Api";
const Auth = () => {
	const [email, setemail] = useState("");
	const [password, setpassword] = useState("");
	const [showLogin, setshowLogin] = useState(false);
	const [showSignup, setshowSignup] = useState(false);
	const [Username, setUsername] = useState("");
	const [apiKey, setapiKey] = useState(false);
	const [isError, setisError] = useState(false);
	const [errorMessage, setErrorMessage] = useState("");
	const [isSuccess, setisSuccess] = useState(false);
	const [SuccessMessage, setSuccessMessage] = useState("");
	const [Loading, setLoading] = useState(true);

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
			if (res_data.isAuthenticated === false) {
				setshowLogin(true);
				setLoading(false);
			} else {
				setshowLogin(false);
				setLoading(false);

				setapiKey(res_data.api_token);
			}
		}
		checkLogin();
	}, []);

	const loginApi = async () => {
		const data = { email: email, password: password };
		await API.post("/login", { ...data })
			.then((res) => {
				console.log(res.data);
				console.log(res.data.isAuthenticated);
				if (res.data.token) {
					localStorage.setItem("jwt", res.data.token);
					setshowLogin(false);
					setshowSignup(false);
					setSuccessMessage("Logged In");
					setisSuccess(true);
				} else {
					setErrorMessage("Error Loging in Check your Email and Password");
					setisError(true);
				}
			})
			.catch((err) => {
				console.log(err);
			});
	};

	const signupApi = async () => {
		const data = { email: email, password: password, username: Username };
		await API.post("/signup", { ...data })
			.then((res) => {
				console.log(res);
				setSuccessMessage("Signed Up");
				setisSuccess(true);
			})
			.catch((err) => {
				console.log(err);
				setErrorMessage("Error Signing Up in Check your Email and Password");
				setisError(true);
			});
	};

	const loginJsx = () => {
		return (
			<CardBody>
				<Container>
					<Row>
						<Col xs={5} style={{ margin: "auto" }}>
							<form
								onSubmit={(e) => {
									e.preventDefault();
									loginApi();
								}}>
								<div class='form-group'>
									<label for='exampleInputEmail1'>Email</label>
									<input
										class='form-control'
										placeholder='Email'
										type='email'
										value={email}
										onChange={(e) => setemail(e.target.value)}
									/>
								</div>
								<div class='form-group'>
									<label for='exampleInputEmail1'>Password</label>
									<input
										class='form-control'
										placeholder='Password'
										type='password'
										value={password}
										onChange={(e) => setpassword(e.target.value)}
									/>
								</div>
								<button
									style={{ margin: "20px", marginTop: "24px" }}
									type='submit'
									class='btn btn-primary'>
									Login
								</button>
								<button
									style={{ margin: "20px", marginTop: "24px" }}
									onClick={(e) => {
										e.preventDefault();
										setshowSignup(true);
										setshowLogin(false);
									}}
									class='btn btn-primary'>
									SignUp
								</button>
							</form>
						</Col>
					</Row>
				</Container>
			</CardBody>
		);
	};

	const signupJsx = () => {
		return (
			<CardBody>
				<Container>
					<Row>
						<Col xs={5} style={{ margin: "auto" }}>
							<form
								onSubmit={(e) => {
									e.preventDefault();
									signupApi();
								}}>
								<div class='form-group'>
									<label for='exampleInputEmail1'>Username</label>
									<input
										class='form-control'
										placeholder='Username'
										type='text'
										value={Username}
										onChange={(e) => setUsername(e.target.value)}
									/>
								</div>
								<div class='form-group'>
									<label for='exampleInputEmail1'>Email</label>
									<input
										class='form-control'
										placeholder='Email'
										type='email'
										value={email}
										onChange={(e) => setemail(e.target.value)}
									/>
								</div>
								<div class='form-group'>
									<label for='exampleInputEmail1'>Password</label>
									<input
										class='form-control'
										placeholder='Password'
										type='password'
										value={password}
										onChange={(e) => setpassword(e.target.value)}
									/>
								</div>
								<button
									style={{ margin: "20px", marginTop: "24px" }}
									type='submit'
									class='btn btn-primary'>
									Sign Up
								</button>
								<button
									style={{ margin: "20px", marginTop: "24px" }}
									class='btn btn-primary'
									onClick={(e) => {
										e.preventDefault();
										setshowSignup(false);
										setshowLogin(true);
									}}>
									Login
								</button>
							</form>
						</Col>
					</Row>
				</Container>
			</CardBody>
		);
	};
	return (
		<>
			<Header
				title='Authenticate To Train Models'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'
			/>
			<Container fluid className='contant-container'>
				{Loading ? (
					<Row>
						<Col>
							<h3>Loading...</h3>
						</Col>
					</Row>
				) : null}
				<Row>
					{apiKey ? (
						<Col>
							<h2>Your Api Key:</h2>
							<h3>{apiKey}</h3>
							<Button
								onClick={(e) => {
									e.preventDefault();
									localStorage.clear();
									window.location.reload();
								}}>
								Sign Out
							</Button>
						</Col>
					) : null}
					{showLogin ? <Col> {loginJsx()} </Col> : null}
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
					{showSignup ? <Col>{signupJsx()}</Col> : null}
				</Row>
			</Container>
		</>
	);
};

export default Auth;
