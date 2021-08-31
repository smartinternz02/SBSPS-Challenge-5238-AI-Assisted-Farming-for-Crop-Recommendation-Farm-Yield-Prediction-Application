import axios from "axios";

export default axios.create({
	baseURL: `https://agrioracle-backend.herokuapp.com/`,
});
