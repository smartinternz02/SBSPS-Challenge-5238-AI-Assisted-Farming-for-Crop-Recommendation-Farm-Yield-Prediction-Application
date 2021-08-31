import React, { useState, useEffect } from "react";
import "./css/HomeCards.scss";
import img1 from "../images/farmer-holds-rice-hand.jpg";
import img2 from "../images/potato-plantations-grow-field-vegetable-rows-farming-agriculture-landscape.jpg";
import img3 from "../images/male-farmer-is-working-field-his-using-mobile-phone-with-innovation-technology-smart-farm-system.jpg";
import img4 from "../images/half-field-is-planted-with-carrot-plantation-second-part-is-ready-sowing.jpg";

const HomeCards = (props) => {
	const [aboutUs, setaboutUs] = useState(props.aboutus);
	const [tools, setTools] = useState(props.tools);

	useEffect(() => {
		setaboutUs(props.aboutus);
		setTools(props.tools);
	}, []);
	return (
		<>
			{aboutUs ? (
				<div>
					<div className='blog-card'>
						<div className='meta'>
							<div
								className='photo'
								style={{
									backgroundImage: `url(${img1})`,
								}}></div>
						</div>
						<div className='description'>
							<h1>Overview</h1>
							<h2>Our Vision</h2>
							<p>
								Agriculture is very crucial to India's Market. Around 60 percent
								of the total land in the country is used for agriculture to meet
								the needs of 1.2 billion people, so improving crop production is
								therefore seen as a significant aspect of agriculture. Farmers
								have been utilizing age-old ways to anticipate the best planting
								date for generations. Typically, they would sow in early June to
								take advantage of the monsoon season, which ran from June to
								August. However, changing weather patterns have resulted in
								unpredictable monsoons in the last decade, resulting in low crop
								yields. Nowadays machine learning algorithms are efficiently
								used in the agriculture field for various purposes. The main aim
								of machine learning is to train the machine to behave like
								humans. The ML has the capability to perform different
								calculations and predictions very effectively with minimum time
							</p>
						</div>
					</div>
					<div className='blog-card alt'>
						<div className='meta'>
							<div
								className='photo'
								style={{
									backgroundImage: `url(${img2})`,
								}}></div>
						</div>
						<div className='description'>
							<h1>Purpose</h1>
							<h2>Our Purpose</h2>
							<p>
								The purpose of this project is to provide a solution to the
								farmers so that they can cultivate the best profitable crop in
								their soil and get every insights of that crop making it one
								stop solution for the farmer.
							</p>
						</div>
					</div>
				</div>
			) : null}

			{tools ? (
				<div>
					<div className='blog-card'>
						<div className='meta'>
							<div
								className='photo'
								style={{
									backgroundImage: `url(${img3})`,
								}}></div>
						</div>
						<div className='description'>
							<h1>Crop Recommendation</h1>
							<h2>Crop Recommendation based on weather and soil</h2>
							<p>
								{" "}
								We are using Seven Parameters In our Trained Model to Suggest
								The best 5 Crops out of 22 Crops to Harvest. The Parameters are
								Temperature, Humidity, Rainfall (Which are based on location)
								and Nitrogen(N), Phosphorus (P), calcium(k), PH(Which we will
								take using IOT device or from a manual Input).
							</p>
						</div>
					</div>
					<div className='blog-card alt'>
						<div className='meta'>
							<div
								className='photo'
								style={{
									backgroundImage: `url(${img4})`,
								}}></div>
						</div>
						<div className='description'>
							<h1>Crop Yield Prediction</h1>
							<h2>Crop Yield Prediction based on season and location</h2>
							<p>
								In this service, we predict the yield of the crop using location
								and season. In location the parameters are City/State, we also
								use area as the parameter to get the proper value for production
								and in season we only need the season name. This service also
								let’s the farmer know the approximate profit/loss when he will
								feed the cost of the crop that he has cultivated.
							</p>
						</div>
					</div>
				</div>
			) : null}
		</>
	);
};

export default HomeCards;
