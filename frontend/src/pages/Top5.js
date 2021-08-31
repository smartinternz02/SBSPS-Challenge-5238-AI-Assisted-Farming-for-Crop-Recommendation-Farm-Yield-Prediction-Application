import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import { Container, Col, Row } from "reactstrap";
import { Table } from "react-bootstrap";
import API from "../utills/Api";
const Top5 = () => {
	const [result, setresult] = useState();
	const [show, setshow] = useState(false);
	const [isLoading, setisLoading] = useState(true);

	useEffect(() => {
		async function Top5() {
			let response = await API.get("/top5");
			response = await response;
			let res_data = { ...response.data };
			console.log(res_data);
			setresult(res_data);
			setshow(true);
			setisLoading(false);
		}
		Top5();
	}, []);

	return (
		<>
			<Header
				title='Top 5 Gainers and Loosers'
				desc1='This is a simple hero unit, a simple Jumbotron-style component
								for calling extra attention to featured content or information.'
				desc2='It uses utility classes for typography and spacing to space
                content out within the larger container.'
			/>
			{isLoading ? (
				<Container fluid className='contant-container'>
					<Row>
						<Col>
							<h3 style={{ textAlign: "center" }}>Loading Top5's.....</h3>
						</Col>
					</Row>
				</Container>
			) : null}
			{show ? (
				<Container fluid className='contant-container'>
					<Row>
						<Col>
							<h2 style={{ textAlign: "center", fontWeight: "bold" }}>
								Top Five Gainers and Loosers
							</h2>
						</Col>
					</Row>
					<Row>
						<Col style={{ margin: "auto", padding: "25px" }} xs={4}>
							<h3
								style={{
									textAlign: "center",
									fontWeight: "bold",
									margin: "50px",
								}}>
								Top 5 Gainers
							</h3>
							<Table striped bordered hover>
								<thead>
									<tr>
										<th>#</th>
										<th>Name</th>
										<th>Current Price</th>
										<th>Previous Month Price</th>
										<th>Current Month Prediction</th>
										<th>Previous Month Prediction</th>
										<th>Change Ammount</th>
									</tr>
								</thead>
								<tbody>
									{result.top5Winner.map((crop, idx) => {
										return (
											<tr>
												<td>{idx + 1}</td>
												<td>{crop[0]}</td>
												<td>{crop[1]}</td>
												<td>{crop[2]}</td>
												<td>{crop[3]}</td>
												<td>{crop[4]}</td>
												<td>{crop[5]}</td>
											</tr>
										);
									})}
								</tbody>
							</Table>
						</Col>
						<Col style={{ margin: "auto", padding: "25px" }} xs={4}>
							<h3
								style={{
									textAlign: "center",
									fontWeight: "bold",
									margin: "50px",
								}}>
								Top 5 Loosers
							</h3>
							<Table striped bordered hover>
								<thead>
									<tr>
										<th>#</th>
										<th>Name</th>
										<th>Current Price</th>
										<th>Previous Month Price</th>
										<th>Current Month Prediction</th>
										<th>Previous Month Prediction</th>
										<th>Change Ammount</th>
									</tr>
								</thead>
								<tbody>
									{result.top5Loosers.map((crop, idx) => {
										return (
											<tr>
												<td>{idx + 1}</td>
												<td>{crop[0]}</td>
												<td>{crop[1]}</td>
												<td>{crop[2]}</td>
												<td>{crop[3]}</td>
												<td>{crop[4]}</td>
												<td>{crop[5]}</td>
											</tr>
										);
									})}
								</tbody>
							</Table>
						</Col>
					</Row>
				</Container>
			) : null}
		</>
	);
};

export default Top5;
