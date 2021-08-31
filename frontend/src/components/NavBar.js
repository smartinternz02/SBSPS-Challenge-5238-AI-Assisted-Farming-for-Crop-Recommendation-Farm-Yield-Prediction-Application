import "./css/NavBar.css";
import {
	AppBar,
	Toolbar,
	Typography,
	makeStyles,
	Button,
	IconButton,
	Drawer,
	Link,
	MenuItem,
} from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import React, { useState, useEffect } from "react";
import { Link as RouterLink } from "react-router-dom";

const headersData = [
	{
		label: "Crop Recomendation",
		href: "/crop-recomendation",
	},
	{
		label: "Yield Finder",
		href: "/yield-finder",
	},
	{
		label: "Price Predictions",
		href: "/price-finder",
	},
	{ label: "Train Your Model", href: "/train-model" },
	{ label: "Api Docs", href: "/apidoc" },
	{ label: "Top 5", href: "/top-5" },

	{
		label: `${
			localStorage.getItem("jwt") === null ? "Login/Signup" : "ApiKey/Signout"
		}`,
		href: "/auth",
	},
];

const useStyles = makeStyles(() => ({
	header: {
		backgroundColor: "#161616",
		paddingRight: "79px",
		paddingLeft: "118px",
		"@media (max-width: 900px)": {
			paddingLeft: 0,
		},
	},
	logo: {
		fontFamily: "Work Sans, sans-serif",
		fontWeight: 600,
		color: "#FFFEFE",
		textAlign: "left",
	},
	menuButton: {
		fontFamily: "Open Sans, sans-serif",
		fontWeight: 700,
		size: "18px",
		marginLeft: "38px",
	},
	toolbar: {
		display: "flex",
		justifyContent: "space-between",
	},
	drawerContainer: {
		padding: "20px 30px",
	},
}));

export default function Header() {
	const { header, logo, menuButton, toolbar, drawerContainer } = useStyles();

	const [state, setState] = useState({
		mobileView: false,
		drawerOpen: false,
	});

	const { mobileView, drawerOpen } = state;

	useEffect(() => {
		const setResponsiveness = () => {
			return window.innerWidth < 900
				? setState((prevState) => ({ ...prevState, mobileView: true }))
				: setState((prevState) => ({ ...prevState, mobileView: false }));
		};

		setResponsiveness();

		window.addEventListener("resize", () => setResponsiveness());

		return () => {
			window.removeEventListener("resize", () => setResponsiveness());
		};
	}, []);

	const displayDesktop = () => {
		return (
			<Toolbar className={toolbar}>
				{femmecubatorLogo}
				<div>{getMenuButtons()}</div>
			</Toolbar>
		);
	};

	const displayMobile = () => {
		const handleDrawerOpen = () =>
			setState((prevState) => ({ ...prevState, drawerOpen: true }));
		const handleDrawerClose = () =>
			setState((prevState) => ({ ...prevState, drawerOpen: false }));

		return (
			<Toolbar>
				<IconButton
					{...{
						edge: "start",
						color: "inherit",
						"aria-label": "menu",
						"aria-haspopup": "true",
						onClick: handleDrawerOpen,
					}}>
					<MenuIcon />
				</IconButton>
				<Drawer
					{...{
						anchor: "left",
						open: drawerOpen,
						onClose: handleDrawerClose,
					}}>
					<div className={drawerContainer}>{getDrawerChoices()}</div>
				</Drawer>

				<div>{femmecubatorLogo}</div>
			</Toolbar>
		);
	};

	const getDrawerChoices = () => {
		return headersData.map(({ label, href }) => {
			return (
				<Link
					{...{
						component: RouterLink,
						to: href,
						color: "inherit",
						style: { textDecoration: "none" },
						key: label,
					}}>
					<MenuItem>{label}</MenuItem>
				</Link>
			);
		});
	};

	const femmecubatorLogo = (
		<a href='/' style={{ textDecoration: "none" }}>
			<Typography variant='h6' component='h1' className={logo}>
				AgriOracle
			</Typography>
		</a>
	);

	const getMenuButtons = () => {
		return headersData.map(({ label, href }) => {
			return (
				<Button
					{...{
						key: label,
						color: "inherit",
						to: href,
						component: RouterLink,
						className: menuButton,
					}}>
					{label}
				</Button>
			);
		});
	};

	return (
		<header>
			<AppBar className={header}>
				{mobileView ? displayMobile() : displayDesktop()}
			</AppBar>
		</header>
	);
}
