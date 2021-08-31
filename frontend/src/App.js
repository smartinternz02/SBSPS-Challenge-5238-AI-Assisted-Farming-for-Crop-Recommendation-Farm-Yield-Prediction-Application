import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "./pages/Home";
import PriceFinder from "./pages/PriceFinder";
import YieldFinder from "./pages/YieldFinder";
import CropRecomendation from "./pages/CropRecomendation";
import TrainModel from "./pages/TrainModel";
import Auth from "./pages/Auth";
import ApiDoc from "./pages/ApiDoc";
import Top5 from "./pages/Top5";

function App() {
	return (
		<Router>
			<div className='App'>
				<Switch>
					<Route exact path='/'>
						<Home></Home>
					</Route>
					<Route exact path='/crop-recomendation'>
						<CropRecomendation />
					</Route>
					<Route exact path='/yield-finder'>
						<YieldFinder></YieldFinder>
					</Route>
					<Route exact path='/price-finder'>
						<PriceFinder></PriceFinder>
					</Route>
					<Route exact path='/train-model'>
						<TrainModel />
					</Route>
					<Route exact path='/auth'>
						<Auth />
					</Route>
					<Route exact path='/apidoc'>
						<ApiDoc />
					</Route>
					<Route exact path='/top-5'>
						<Top5 />
					</Route>
				</Switch>
			</div>
		</Router>
	);
}

export default App;
