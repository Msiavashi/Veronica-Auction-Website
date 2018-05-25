--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: addresses; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.addresses (
    id bigint NOT NULL,
    country character varying(50) NOT NULL,
    state character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    address character varying(255) NOT NULL,
    postal_code character varying(20) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.addresses OWNER TO bidbazi;

--
-- Name: addresses_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.addresses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.addresses_id_seq OWNER TO bidbazi;

--
-- Name: addresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.addresses_id_seq OWNED BY public.addresses.id;


--
-- Name: advertisements; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.advertisements (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    images text NOT NULL,
    link_title character varying(100) NOT NULL,
    show boolean,
    discount integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.advertisements OWNER TO bidbazi;

--
-- Name: advertisements_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.advertisements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.advertisements_id_seq OWNER TO bidbazi;

--
-- Name: advertisements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.advertisements_id_seq OWNED BY public.advertisements.id;


--
-- Name: auction_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auction_plans (
    id bigint NOT NULL,
    price numeric(20,4) NOT NULL,
    max_offers integer NOT NULL,
    auction_id bigint,
    plan_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.auction_plans OWNER TO bidbazi;

--
-- Name: auction_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.auction_plans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auction_plans_id_seq OWNER TO bidbazi;

--
-- Name: auction_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.auction_plans_id_seq OWNED BY public.auction_plans.id;


--
-- Name: auctions; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auctions (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    base_price numeric(20,4) NOT NULL,
    max_price numeric(20,4) NOT NULL,
    max_members bigint NOT NULL,
    ratio integer NOT NULL,
    item_id bigint NOT NULL,
    event_id bigint,
    advertisement_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.auctions OWNER TO bidbazi;

--
-- Name: auctions_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.auctions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auctions_id_seq OWNER TO bidbazi;

--
-- Name: auctions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.auctions_id_seq OWNED BY public.auctions.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.categories (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description character varying(255) NOT NULL,
    icon text,
    category_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.categories OWNER TO bidbazi;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO bidbazi;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.comments (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    likes integer,
    user_id bigint,
    product_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.comments OWNER TO bidbazi;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO bidbazi;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.events (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    is_active boolean,
    discount integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.events OWNER TO bidbazi;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO bidbazi;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: garanties; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.garanties (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    price numeric(20,4) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.garanties OWNER TO bidbazi;

--
-- Name: garanties_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.garanties_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.garanties_id_seq OWNER TO bidbazi;

--
-- Name: garanties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.garanties_id_seq OWNED BY public.garanties.id;


--
-- Name: garanty_products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.garanty_products (
    garanty_id bigint,
    product_id bigint
);


ALTER TABLE public.garanty_products OWNER TO bidbazi;

--
-- Name: gifts; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.gifts (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    amount numeric(20,4) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.gifts OWNER TO bidbazi;

--
-- Name: gifts_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.gifts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gifts_id_seq OWNER TO bidbazi;

--
-- Name: gifts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.gifts_id_seq OWNED BY public.gifts.id;


--
-- Name: guest_messages; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.guest_messages (
    id bigint NOT NULL,
    full_name character varying(128) NOT NULL,
    email character varying(128) NOT NULL,
    website character varying(256),
    message character varying(1024) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.guest_messages OWNER TO bidbazi;

--
-- Name: guest_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.guest_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.guest_messages_id_seq OWNER TO bidbazi;

--
-- Name: guest_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.guest_messages_id_seq OWNED BY public.guest_messages.id;


--
-- Name: insurances; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.insurances (
    id bigint NOT NULL,
    company character varying(100) NOT NULL,
    description text NOT NULL,
    price numeric(20,4) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.insurances OWNER TO bidbazi;

--
-- Name: insurances_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.insurances_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.insurances_id_seq OWNER TO bidbazi;

--
-- Name: insurances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.insurances_id_seq OWNED BY public.insurances.id;


--
-- Name: inventories; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.inventories (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    desciption character varying(255) NOT NULL,
    address_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.inventories OWNER TO bidbazi;

--
-- Name: inventories_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.inventories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventories_id_seq OWNER TO bidbazi;

--
-- Name: inventories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.inventories_id_seq OWNED BY public.inventories.id;


--
-- Name: inventory_products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.inventory_products (
    inventory_id bigint,
    product_id bigint
);


ALTER TABLE public.inventory_products OWNER TO bidbazi;

--
-- Name: items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.items (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    price numeric(20,4) NOT NULL,
    discount integer,
    details text,
    images text NOT NULL,
    product_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.items OWNER TO bidbazi;

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.items_id_seq OWNER TO bidbazi;

--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: manufacture_products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.manufacture_products (
    manufacture_id bigint,
    product_id bigint
);


ALTER TABLE public.manufacture_products OWNER TO bidbazi;

--
-- Name: manufactures; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.manufactures (
    id bigint NOT NULL,
    name character varying(25) NOT NULL,
    country character varying(100) NOT NULL,
    desciption text NOT NULL,
    details text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.manufactures OWNER TO bidbazi;

--
-- Name: manufactures_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.manufactures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.manufactures_id_seq OWNER TO bidbazi;

--
-- Name: manufactures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.manufactures_id_seq OWNED BY public.manufactures.id;


--
-- Name: offers; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.offers (
    id bigint NOT NULL,
    total_price numeric(20,4) NOT NULL,
    current_bids integer NOT NULL,
    win boolean,
    user_plan_id bigint,
    auction_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.offers OWNER TO bidbazi;

--
-- Name: offers_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.offers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.offers_id_seq OWNER TO bidbazi;

--
-- Name: offers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.offers_id_seq OWNED BY public.offers.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.order_items (
    order_id bigint,
    item_id bigint
);


ALTER TABLE public.order_items OWNER TO bidbazi;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    desciption text,
    status integer,
    register_user boolean,
    total_cost numeric(20,4) NOT NULL,
    user_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.orders OWNER TO bidbazi;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO bidbazi;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payment_methods (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    details text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.payment_methods OWNER TO bidbazi;

--
-- Name: payment_methods_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.payment_methods_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_methods_id_seq OWNER TO bidbazi;

--
-- Name: payment_methods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.payment_methods_id_seq OWNED BY public.payment_methods.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    "GUID" character varying(50),
    amount numeric(20,4) NOT NULL,
    status integer NOT NULL,
    details text,
    payment_method_id bigint NOT NULL,
    order_id bigint NOT NULL,
    user_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.payments OWNER TO bidbazi;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_id_seq OWNER TO bidbazi;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.plans (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    desciption text NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.plans OWNER TO bidbazi;

--
-- Name: plans_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.plans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.plans_id_seq OWNER TO bidbazi;

--
-- Name: plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.plans_id_seq OWNED BY public.plans.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.products (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    desciption text NOT NULL,
    quantity integer NOT NULL,
    details text,
    category_id bigint,
    manufacture_id bigint,
    advertisement_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.products OWNER TO bidbazi;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO bidbazi;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.roles (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.roles OWNER TO bidbazi;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO bidbazi;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: shipment_methods; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.shipment_methods (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    price numeric(20,4),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.shipment_methods OWNER TO bidbazi;

--
-- Name: shipment_methods_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.shipment_methods_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shipment_methods_id_seq OWNER TO bidbazi;

--
-- Name: shipment_methods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.shipment_methods_id_seq OWNED BY public.shipment_methods.id;


--
-- Name: shipments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.shipments (
    id bigint NOT NULL,
    shipment_method_id bigint,
    insurance_id bigint,
    send_date timestamp without time zone,
    recieve_date timestamp without time zone,
    status boolean,
    payment_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.shipments OWNER TO bidbazi;

--
-- Name: shipments_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.shipments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shipments_id_seq OWNER TO bidbazi;

--
-- Name: shipments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.shipments_id_seq OWNED BY public.shipments.id;


--
-- Name: user_auction_likes; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_auction_likes (
    user_id bigint,
    auction_id bigint,
    date timestamp without time zone
);


ALTER TABLE public.user_auction_likes OWNER TO bidbazi;

--
-- Name: user_auction_participations; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_auction_participations (
    id bigint NOT NULL,
    auction_id bigint,
    user_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.user_auction_participations OWNER TO bidbazi;

--
-- Name: user_auction_participations_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.user_auction_participations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_auction_participations_id_seq OWNER TO bidbazi;

--
-- Name: user_auction_participations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.user_auction_participations_id_seq OWNED BY public.user_auction_participations.id;


--
-- Name: user_auction_views; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_auction_views (
    user_id bigint,
    auction_id bigint,
    count integer,
    ip character varying(50),
    date timestamp without time zone
);


ALTER TABLE public.user_auction_views OWNER TO bidbazi;

--
-- Name: user_gifts; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_gifts (
    user_id bigint,
    gift_id bigint,
    used boolean
);


ALTER TABLE public.user_gifts OWNER TO bidbazi;

--
-- Name: user_messages; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_messages (
    id bigint NOT NULL,
    user_id bigint,
    title character varying(128) NOT NULL,
    subject integer NOT NULL,
    message text NOT NULL,
    file character varying(1024),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.user_messages OWNER TO bidbazi;

--
-- Name: user_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.user_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_messages_id_seq OWNER TO bidbazi;

--
-- Name: user_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.user_messages_id_seq OWNED BY public.user_messages.id;


--
-- Name: user_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_plans (
    id bigint NOT NULL,
    user_id bigint,
    auction_id bigint,
    auction_plan_id bigint,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.user_plans OWNER TO bidbazi;

--
-- Name: user_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.user_plans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_plans_id_seq OWNER TO bidbazi;

--
-- Name: user_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.user_plans_id_seq OWNED BY public.user_plans.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_roles (
    user_id bigint,
    role_id bigint
);


ALTER TABLE public.user_roles OWNER TO bidbazi;

--
-- Name: users; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(255) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    work_place character varying(100),
    mobile character varying(15) NOT NULL,
    email character varying(255),
    password character varying(100) NOT NULL,
    avatar character varying(300),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    invitor character varying(255),
    credit numeric(20,4),
    address_id bigint,
    alias_name character varying(255)
);


ALTER TABLE public.users OWNER TO bidbazi;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO bidbazi;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: addresses id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);


--
-- Name: advertisements id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.advertisements ALTER COLUMN id SET DEFAULT nextval('public.advertisements_id_seq'::regclass);


--
-- Name: auction_plans id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_plans ALTER COLUMN id SET DEFAULT nextval('public.auction_plans_id_seq'::regclass);


--
-- Name: auctions id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auctions ALTER COLUMN id SET DEFAULT nextval('public.auctions_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: garanties id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.garanties ALTER COLUMN id SET DEFAULT nextval('public.garanties_id_seq'::regclass);


--
-- Name: gifts id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts ALTER COLUMN id SET DEFAULT nextval('public.gifts_id_seq'::regclass);


--
-- Name: guest_messages id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.guest_messages ALTER COLUMN id SET DEFAULT nextval('public.guest_messages_id_seq'::regclass);


--
-- Name: insurances id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurances ALTER COLUMN id SET DEFAULT nextval('public.insurances_id_seq'::regclass);


--
-- Name: inventories id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventories ALTER COLUMN id SET DEFAULT nextval('public.inventories_id_seq'::regclass);


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Name: manufactures id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.manufactures ALTER COLUMN id SET DEFAULT nextval('public.manufactures_id_seq'::regclass);


--
-- Name: offers id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offers ALTER COLUMN id SET DEFAULT nextval('public.offers_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: payment_methods id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_methods ALTER COLUMN id SET DEFAULT nextval('public.payment_methods_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: plans id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.plans ALTER COLUMN id SET DEFAULT nextval('public.plans_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: shipment_methods id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipment_methods ALTER COLUMN id SET DEFAULT nextval('public.shipment_methods_id_seq'::regclass);


--
-- Name: shipments id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments ALTER COLUMN id SET DEFAULT nextval('public.shipments_id_seq'::regclass);


--
-- Name: user_auction_participations id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_participations ALTER COLUMN id SET DEFAULT nextval('public.user_auction_participations_id_seq'::regclass);


--
-- Name: user_messages id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_messages ALTER COLUMN id SET DEFAULT nextval('public.user_messages_id_seq'::regclass);


--
-- Name: user_plans id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans ALTER COLUMN id SET DEFAULT nextval('public.user_plans_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.addresses (id, country, state, city, address, postal_code, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: advertisements; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.advertisements (id, title, description, images, link_title, show, discount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: auction_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auction_plans (id, price, max_offers, auction_id, plan_id, created_at, updated_at) FROM stdin;
1	50000.0000	20	1	1	2018-05-21 20:41:30	2018-05-21 20:41:30
2	30000.0000	20	1	2	2018-05-21 20:41:47	2018-05-21 20:41:47
3	20000.0000	10	1	3	2018-05-21 20:42:04	2018-05-21 20:42:04
4	40000.0000	40	2	1	2018-05-21 21:38:15	2018-05-21 21:38:15
5	30000.0000	30	2	2	2018-05-21 21:38:30	2018-05-21 21:38:30
\.


--
-- Data for Name: auctions; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auctions (id, title, description, start_date, end_date, base_price, max_price, max_members, ratio, item_id, event_id, advertisement_id, created_at, updated_at) FROM stdin;
2	حراجی گوشی آیفون	این هم یک حراجی تست است	2018-05-25 19:09:00	2018-05-22 22:49:00	5000000.0000	7000000.0000	50	10	2	\N	\N	2018-05-21 19:49:37	2018-05-21 19:49:37
1	حراجی آیفون ایکس 	این گوشی خوبی است برای حراجی 	2018-05-25 17:10:00	2018-05-22 23:47:00	4000000.0000	5500000.0000	30	5	1	\N	\N	2018-05-21 19:47:11	2018-05-21 19:47:11
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.categories (id, title, description, icon, category_id, created_at, updated_at) FROM stdin;
1	موبایل	این دسته بندی موبایل است	['clock.png']	\N	2018-05-21 19:42:52	2018-05-21 19:42:52
2	لپ تاپ	این دسته بندی لپ تاپ است	['for6.png']	\N	2018-05-21 19:43:06	2018-05-21 19:43:06
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.comments (id, title, message, likes, user_id, product_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.events (id, title, description, start_date, end_date, is_active, discount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: garanties; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.garanties (id, title, description, price, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: garanty_products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.garanty_products (garanty_id, product_id) FROM stdin;
\.


--
-- Data for Name: gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.gifts (id, title, description, amount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: guest_messages; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.guest_messages (id, full_name, email, website, message, created_at) FROM stdin;
\.


--
-- Data for Name: insurances; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.insurances (id, company, description, price, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: inventories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventories (id, name, desciption, address_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: inventory_products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventory_products (inventory_id, product_id) FROM stdin;
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.items (id, title, description, price, discount, details, images, product_id, created_at, updated_at) FROM stdin;
1	۱۲۸ گیگابایت	این یک گوشی بی نظیر است	6500000.0000	10		['ad1.jpg', 'ad2.jpg']	1	2018-05-21 19:44:07	2018-05-21 19:44:07
2	۲۵۶ گیگابایت	این هم تست است	7500000.0000	5		['4.jpg', '7.jpg']	1	2018-05-21 19:45:27	2018-05-21 19:45:27
\.


--
-- Data for Name: manufacture_products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufacture_products (manufacture_id, product_id) FROM stdin;
\.


--
-- Data for Name: manufactures; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufactures (id, name, country, desciption, details, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: offers; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.offers (id, total_price, current_bids, win, user_plan_id, auction_id, created_at, updated_at) FROM stdin;
773	4005000.0000	19	f	47	1	2018-05-25 17:00:03.210641	2018-05-25 17:00:03.210868
774	4010000.0000	19	f	48	1	2018-05-25 17:00:07.563651	2018-05-25 17:00:07.563882
775	4015000.0000	18	f	47	1	2018-05-25 17:00:10.078869	2018-05-25 17:00:10.07903
776	4020000.0000	18	f	48	1	2018-05-25 17:00:11.65055	2018-05-25 17:00:11.650721
777	4025000.0000	17	f	47	1	2018-05-25 17:00:13.301495	2018-05-25 17:00:13.301651
778	4030000.0000	17	f	48	1	2018-05-25 17:00:15.402555	2018-05-25 17:00:15.402826
779	4035000.0000	16	f	47	1	2018-05-25 17:00:19.118239	2018-05-25 17:00:19.11839
780	4040000.0000	16	t	48	1	2018-05-25 17:00:21.559752	2018-05-25 17:00:21.559955
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.order_items (order_id, item_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.orders (id, desciption, status, register_user, total_cost, user_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payment_methods (id, title, description, details, created_at, updated_at) FROM stdin;
1	پرداخت از حساب	از موجودی حساب خود پرداخت کنید		2018-05-21 22:12:42	2018-05-21 22:12:42
2	پرداخت از کارت بانکی	تمامی کارتهای عضو شبکه شتاب		2018-05-21 22:13:11	2018-05-21 22:13:11
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payments (id, "GUID", amount, status, details, payment_method_id, order_id, user_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.plans (id, title, desciption, created_at, updated_at) FROM stdin;
1	طلایی	این طلایی است	2018-05-21 19:46:25	2018-05-21 19:46:25
2	نقره ای	این نقره ای است	2018-05-21 19:46:36	2018-05-21 19:46:36
3	برنزی	این برنزی است	2018-05-21 19:46:47	2018-05-21 19:46:47
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.products (id, title, desciption, quantity, details, category_id, manufacture_id, advertisement_id, created_at, updated_at) FROM stdin;
1	آیفون ایکس	این یک آیفون ایکس است	10		1	\N	\N	2018-05-21 19:43:30	2018-05-21 19:43:30
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.roles (id, name, description, created_at, updated_at) FROM stdin;
1	admin	this is admin role	2018-05-21 19:37:04	2018-05-21 19:37:04
2	regular	this is regular role	2018-05-21 19:37:16	2018-05-21 19:37:16
\.


--
-- Data for Name: shipment_methods; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.shipment_methods (id, title, description, price, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.shipments (id, shipment_method_id, insurance_id, send_date, recieve_date, status, payment_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_auction_likes; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_likes (user_id, auction_id, date) FROM stdin;
\.


--
-- Data for Name: user_auction_participations; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_participations (id, auction_id, user_id, created_at, updated_at) FROM stdin;
63	1	2	2018-05-22 18:48:26.037786	2018-05-22 18:48:26.037916
64	1	3	2018-05-22 18:56:23.29873	2018-05-22 18:56:23.29887
65	2	3	2018-05-22 21:38:59.883021	2018-05-22 21:38:59.883216
66	2	2	2018-05-22 21:39:25.63698	2018-05-22 21:39:25.637117
\.


--
-- Data for Name: user_auction_views; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_views (user_id, auction_id, count, ip, date) FROM stdin;
\.


--
-- Data for Name: user_gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_gifts (user_id, gift_id, used) FROM stdin;
\.


--
-- Data for Name: user_messages; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_messages (id, user_id, title, subject, message, file, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_plans (id, user_id, auction_id, auction_plan_id, created_at, updated_at) FROM stdin;
47	2	1	2	2018-05-22 18:48:26.04575	2018-05-22 18:48:26.045906
48	3	1	2	2018-05-22 18:56:23.308002	2018-05-22 18:56:23.308129
49	3	2	5	2018-05-22 21:38:59.891664	2018-05-22 21:38:59.891843
50	2	2	5	2018-05-22 21:39:25.643508	2018-05-22 21:39:25.6437
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_roles (user_id, role_id) FROM stdin;
2	2
3	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.users (id, username, first_name, last_name, work_place, mobile, email, password, avatar, created_at, updated_at, invitor, credit, address_id, alias_name) FROM stdin;
3	ali	\N	\N	\N	1	\N	$pbkdf2-sha256$29000$0hoj5Lz3PieEEIIQIqT0Pg$JHjCAw8rIpNuWjnpC94TXnCrxGfmM8CTD676m9afiDE	['004.png']	2018-05-21 20:48:52	2018-05-21 20:48:52	\N	-240000.0000	\N	\N
2	mr_asadi	محمدرضا	اسدی	\N	09360284814	\N	$pbkdf2-sha256$29000$D4FQKgXgnPNeS2nNuReiFA$EHoDqYnIo0X9JoBOikXgC5z8NWzimcvhm97.45GzRMQ	['005.png']	2018-05-21 19:37:35	2018-05-21 19:37:35	\N	-100000.0000	\N	\N
\.


--
-- Name: addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.addresses_id_seq', 1, false);


--
-- Name: advertisements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.advertisements_id_seq', 1, false);


--
-- Name: auction_plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.auction_plans_id_seq', 5, true);


--
-- Name: auctions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.auctions_id_seq', 2, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.categories_id_seq', 2, true);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.events_id_seq', 1, false);


--
-- Name: garanties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.garanties_id_seq', 1, false);


--
-- Name: gifts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.gifts_id_seq', 1, false);


--
-- Name: guest_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.guest_messages_id_seq', 1, false);


--
-- Name: insurances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.insurances_id_seq', 1, false);


--
-- Name: inventories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.inventories_id_seq', 1, false);


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.items_id_seq', 2, true);


--
-- Name: manufactures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.manufactures_id_seq', 1, false);


--
-- Name: offers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.offers_id_seq', 780, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: payment_methods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.payment_methods_id_seq', 2, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.plans_id_seq', 3, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.products_id_seq', 1, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- Name: shipment_methods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.shipment_methods_id_seq', 1, false);


--
-- Name: shipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.shipments_id_seq', 1, false);


--
-- Name: user_auction_participations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.user_auction_participations_id_seq', 66, true);


--
-- Name: user_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.user_messages_id_seq', 1, false);


--
-- Name: user_plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.user_plans_id_seq', 50, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: advertisements advertisements_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.advertisements
    ADD CONSTRAINT advertisements_pkey PRIMARY KEY (id);


--
-- Name: auction_plans auction_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_plans
    ADD CONSTRAINT auction_plans_pkey PRIMARY KEY (id);


--
-- Name: auctions auctions_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: garanties garanties_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.garanties
    ADD CONSTRAINT garanties_pkey PRIMARY KEY (id);


--
-- Name: gifts gifts_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT gifts_pkey PRIMARY KEY (id);


--
-- Name: guest_messages guest_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.guest_messages
    ADD CONSTRAINT guest_messages_pkey PRIMARY KEY (id);


--
-- Name: insurances insurances_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurances
    ADD CONSTRAINT insurances_pkey PRIMARY KEY (id);


--
-- Name: inventories inventories_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventories
    ADD CONSTRAINT inventories_pkey PRIMARY KEY (id);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- Name: manufactures manufactures_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.manufactures
    ADD CONSTRAINT manufactures_pkey PRIMARY KEY (id);


--
-- Name: offers offers_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: plans plans_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: shipment_methods shipment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipment_methods
    ADD CONSTRAINT shipment_methods_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (id);


--
-- Name: user_auction_participations user_auction_participations_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_participations
    ADD CONSTRAINT user_auction_participations_pkey PRIMARY KEY (id);


--
-- Name: user_messages user_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_messages
    ADD CONSTRAINT user_messages_pkey PRIMARY KEY (id);


--
-- Name: user_plans user_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_uc; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_uc UNIQUE (username);


--
-- Name: auction_plans auction_plans_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_plans
    ADD CONSTRAINT auction_plans_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: auction_plans auction_plans_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_plans
    ADD CONSTRAINT auction_plans_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id);


--
-- Name: auctions auctions_advertisement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_advertisement_id_fkey FOREIGN KEY (advertisement_id) REFERENCES public.advertisements(id);


--
-- Name: auctions auctions_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: auctions auctions_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: categories categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: comments comments_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: garanty_products garanty_products_garanty_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.garanty_products
    ADD CONSTRAINT garanty_products_garanty_id_fkey FOREIGN KEY (garanty_id) REFERENCES public.garanties(id);


--
-- Name: garanty_products garanty_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.garanty_products
    ADD CONSTRAINT garanty_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: inventories inventories_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventories
    ADD CONSTRAINT inventories_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: inventory_products inventory_products_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_products
    ADD CONSTRAINT inventory_products_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventories(id);


--
-- Name: inventory_products inventory_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_products
    ADD CONSTRAINT inventory_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: items items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: manufacture_products manufacture_products_manufacture_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.manufacture_products
    ADD CONSTRAINT manufacture_products_manufacture_id_fkey FOREIGN KEY (manufacture_id) REFERENCES public.manufactures(id);


--
-- Name: manufacture_products manufacture_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.manufacture_products
    ADD CONSTRAINT manufacture_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: offers offers_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: offers offers_user_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_user_plan_id_fkey FOREIGN KEY (user_plan_id) REFERENCES public.user_plans(id);


--
-- Name: order_items order_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: payments payments_payment_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_payment_method_id_fkey FOREIGN KEY (payment_method_id) REFERENCES public.payment_methods(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: products products_advertisement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_advertisement_id_fkey FOREIGN KEY (advertisement_id) REFERENCES public.advertisements(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: products products_manufacture_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_manufacture_id_fkey FOREIGN KEY (manufacture_id) REFERENCES public.manufactures(id);


--
-- Name: shipments shipments_insurance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_insurance_id_fkey FOREIGN KEY (insurance_id) REFERENCES public.insurances(id);


--
-- Name: shipments shipments_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: shipments shipments_shipment_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_shipment_method_id_fkey FOREIGN KEY (shipment_method_id) REFERENCES public.shipment_methods(id);


--
-- Name: user_auction_likes user_auction_likes_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_likes
    ADD CONSTRAINT user_auction_likes_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_auction_likes user_auction_likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_likes
    ADD CONSTRAINT user_auction_likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_auction_participations user_auction_participations_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_participations
    ADD CONSTRAINT user_auction_participations_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_auction_participations user_auction_participations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_participations
    ADD CONSTRAINT user_auction_participations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_auction_views user_auction_views_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_views
    ADD CONSTRAINT user_auction_views_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_auction_views user_auction_views_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auction_views
    ADD CONSTRAINT user_auction_views_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_gifts user_gifts_gift_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_gifts
    ADD CONSTRAINT user_gifts_gift_id_fkey FOREIGN KEY (gift_id) REFERENCES public.gifts(id);


--
-- Name: user_gifts user_gifts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_gifts
    ADD CONSTRAINT user_gifts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_messages user_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_messages
    ADD CONSTRAINT user_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_plans user_plans_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_plans user_plans_auction_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_auction_plan_id_fkey FOREIGN KEY (auction_plan_id) REFERENCES public.auction_plans(id);


--
-- Name: user_plans user_plans_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- PostgreSQL database dump complete
--

