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
    country character varying(50),
    state character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    address character varying(255) NOT NULL,
    postal_code character varying(20) NOT NULL
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
    description character varying(100) NOT NULL,
    link_title character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    auction_id bigint,
    show boolean DEFAULT false,
    product_id bigint,
    images text
);


ALTER TABLE public.advertisements OWNER TO bidbazi;
s
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
-- Name: auction_events; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auction_events (
    auction_id bigint,
    event_id bigint,
    discount numeric(20,4)
);


ALTER TABLE public.auction_events OWNER TO bidbazi;

--
-- Name: auctions; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auctions (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    register_price numeric(20,4) NOT NULL,
    minimum_price numeric(20,4) NOT NULL,
    maximum_price numeric(20,4) NOT NULL,
    max_members bigint,
    item_id bigint
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
    name character varying(100) NOT NULL,
    description character varying(255),
    category_id bigint,
    icon text
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
    message character varying(2048) NOT NULL,
    likes integer,
    date timestamp without time zone NOT NULL,
    user_id bigint,
    product_id bigint
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
    title character varying(255),
    description text,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    active boolean DEFAULT false,
    discount integer DEFAULT 0
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
-- Name: gifts; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.gifts (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    amount numeric(20,4)
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
-- Name: insurance_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.insurance_items (
    insurance_id bigint,
    item_id bigint
);


ALTER TABLE public.insurance_items OWNER TO bidbazi;

--
-- Name: insurances; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.insurances (
    id bigint NOT NULL,
    company_name character varying(100) NOT NULL,
    description text,
    price numeric(20,4) NOT NULL
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
    desciption character varying(255),
    address_id bigint
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
-- Name: inventory_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.inventory_items (
    inventory_id bigint,
    item_id bigint,
    count integer
);


ALTER TABLE public.inventory_items OWNER TO bidbazi;

--
-- Name: items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.items (
    id bigint NOT NULL,
    model character varying(100) NOT NULL,
    description text,
    price numeric(20,4) NOT NULL,
    product_id bigint,
    inventory_id bigint,
    discount integer DEFAULT 0
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
    review text,
    details bytea
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
-- Name: offer; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.offer (
    id bigint NOT NULL,
    offer_price numeric(20,4) NOT NULL,
    date timestamp without time zone,
    status integer,
    win boolean,
    user_id bigint,
    item_id bigint
);


ALTER TABLE public.offer OWNER TO bidbazi;

--
-- Name: offer_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.offer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.offer_id_seq OWNER TO bidbazi;

--
-- Name: offer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.offer_id_seq OWNED BY public.offer.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.order_items (
    item_id bigint,
    order_id bigint
);


ALTER TABLE public.order_items OWNER TO bidbazi;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    create_at timestamp without time zone,
    updated_at timestamp without time zone,
    status boolean,
    user_id bigint,
    shipment_id bigint
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
-- Name: payment_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payment_items (
    payment_id integer,
    item_id bigint
);


ALTER TABLE public.payment_items OWNER TO bidbazi;

--
-- Name: payment_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payment_plans (
    payment_id integer,
    plan_id bigint
);


ALTER TABLE public.payment_plans OWNER TO bidbazi;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    amount numeric(20,4) NOT NULL,
    guid character varying(50),
    date timestamp without time zone,
    method bytea,
    status boolean,
    details bytea,
    user_id bigint
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
    name character varying(100) NOT NULL,
    price numeric(20,4),
    total_offers integer
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
-- Name: product_events; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.product_events (
    product_id bigint,
    event_id bigint,
    discount numeric(20,4)
);


ALTER TABLE public.product_events OWNER TO bidbazi;

--
-- Name: products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.products (
    id bigint NOT NULL,
    name character varying(25) NOT NULL,
    quantity integer NOT NULL,
    review text,
    details bytea,
    category_id bigint,
    manufacture_id bigint,
    advertisement_id bigint,
    images text
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
-- Name: revoked_tokens; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.revoked_tokens (
    id integer NOT NULL,
    jti character varying(120)
);


ALTER TABLE public.revoked_tokens OWNER TO bidbazi;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.revoked_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.revoked_tokens_id_seq OWNER TO bidbazi;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.revoked_tokens_id_seq OWNED BY public.revoked_tokens.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.roles (
    id bigint NOT NULL,
    name character varying(80) NOT NULL,
    description character varying(512)
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
-- Name: shipments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.shipments (
    id bigint NOT NULL,
    company character varying(100) NOT NULL,
    method character varying(100) NOT NULL,
    send_date timestamp without time zone,
    recieve_date timestamp without time zone,
    price numeric(20,4) NOT NULL,
    vehicle character varying(35),
    status boolean,
    insurance_id bigint
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
-- Name: user_auctions; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_auctions (
    auction_id bigint,
    user_id bigint,
    date timestamp without time zone
);


ALTER TABLE public.user_auctions OWNER TO bidbazi;

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
-- Name: user_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_plans (
    user_id bigint,
    plan_id bigint,
    used boolean
);


ALTER TABLE public.user_plans OWNER TO bidbazi;

--
-- Name: user_product_likes; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_product_likes (
    product_id bigint,
    user_id bigint
);


ALTER TABLE public.user_product_likes OWNER TO bidbazi;

--
-- Name: user_product_views; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_product_views (
    product_id bigint,
    user_id bigint,
    ip_address character varying(64),
    date timestamp without time zone
);


ALTER TABLE public.user_product_views OWNER TO bidbazi;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_roles (
    role_id bigint,
    user_id bigint
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
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    invitor character varying(255),
    credit numeric(20,4),
    address_id bigint
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
-- Name: gifts id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts ALTER COLUMN id SET DEFAULT nextval('public.gifts_id_seq'::regclass);


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
-- Name: offer id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer ALTER COLUMN id SET DEFAULT nextval('public.offer_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


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
-- Name: revoked_tokens id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.revoked_tokens ALTER COLUMN id SET DEFAULT nextval('public.revoked_tokens_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: shipments id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments ALTER COLUMN id SET DEFAULT nextval('public.shipments_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.addresses (id, country, state, city, address, postal_code) FROM stdin;
\.


--
-- Data for Name: advertisements; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.advertisements (id, title, description, link_title, created_at, updated_at, auction_id, show, product_id, images) FROM stdin;
3	آی پد	این یک آی پد زیباست	برای یک خرید خوب کلیک کنید شوید	2018-05-06 20:42:55	2018-05-06 20:42:55	4	t	2	['slide3.jpg']
2	تبلیغ جدید	این یک تبلیغ جدید است	شانس خود را امتحان کنید	2018-05-06 19:36:00	2018-05-06 19:36:00	5	t	1	['slide2.png']
4	تبلیغات حراجی زیبا	اینا همش حرفه	بپر تو..!	2018-05-09 05:00:34	2018-05-18 05:00:34	5	t	1	['ad1.jpg']
\.


--
-- Data for Name: auction_events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auction_events (auction_id, event_id, discount) FROM stdin;
4	1	\N
4	2	\N
5	1	\N
\.


--
-- Data for Name: auctions; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auctions (id, name, description, created_at, updated_at, start_date, end_date, register_price, minimum_price, maximum_price, max_members, item_id) FROM stdin;
4	test	test	2018-05-08 10:50:55	2018-05-08 10:50:55	2018-05-07 10:50:55	2018-05-24 10:50:55	3424.0000	43.0000	2.0000	40	4
3	حراجی تست	این یک حراجی تستی است	2018-05-07 16:37:42	2018-05-07 16:37:42	2018-05-07 16:37:42	2018-05-09 16:37:42	150000.0000	10000.0000	200000.0000	40	3
5	حراجی زیبای من	این یک حراجی زیباست	2018-05-09 04:58:43	2018-05-09 04:58:43	2018-05-08 04:58:43	2018-05-17 04:58:43	120000.0000	1230000.0000	1200000.0000	50	3
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.categories (id, name, description, category_id, icon) FROM stdin;
4	تبلت	این دسته بندی مربوط به تبلت است	\N	['for3_2.png']
2	لوازم خانگی	این دسته بندی مربوط به لوازم خانگی است	\N	['for2_2.png']
3	موبایل	این دسته بندی مربوط به موبایل است	\N	['for3_2.png']
1	دیجتال	این دسته بندی لوازم دیجیتالی است	\N	['arrow-down.png']
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.comments (id, title, message, likes, date, user_id, product_id) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.events (id, title, description, start_date, end_date, active, discount) FROM stdin;
1	به مناسبت افتتاح سایت	تخفیف در حراجی های طلایی!	2018-05-01 11:47:43	2018-05-09 11:47:43	t	10
2	حراجی محصولات سایت 	تخفیف در دسته بندی لوازم خانگی! 	2018-05-07 13:54:30	2018-05-07 15:54:00	t	40
\.


--
-- Data for Name: gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.gifts (id, name, amount) FROM stdin;
\.


--
-- Data for Name: insurance_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.insurance_items (insurance_id, item_id) FROM stdin;
2	3
\.


--
-- Data for Name: insurances; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.insurances (id, company_name, description, price) FROM stdin;
1	گارانتی سازگار		12000.0000
2	گارانتی پارامیس		30000.0000
\.


--
-- Data for Name: inventories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventories (id, name, desciption, address_id) FROM stdin;
1	شرکت	انبار مرکزی شرکت	\N
2	ولیعصر	بازارچه رضا - مغازه ۵	\N
\.


--
-- Data for Name: inventory_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventory_items (inventory_id, item_id, count) FROM stdin;
2	3	\N
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.items (id, model, description, price, product_id, inventory_id, discount) FROM stdin;
4	جدیدترین مدل	این یک آیپد جدید است	4300000.0000	2	\N	30
3	۱۲۸ گیگابایت	این یک آیتم از گوشی های زیبای آیفون است	2500000.0000	1	\N	25
\.


--
-- Data for Name: manufacture_products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufacture_products (manufacture_id, product_id) FROM stdin;
\.


--
-- Data for Name: manufactures; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufactures (id, name, country, review, details) FROM stdin;
1	سامسونگ	کره	این توضیحات مربوط به کارخانه سامسونگ است	\N
2	اپل	آمریکا	\r\n	\N
\.


--
-- Data for Name: offer; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.offer (id, offer_price, date, status, win, user_id, item_id) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.order_items (item_id, order_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.orders (id, create_at, updated_at, status, user_id, shipment_id) FROM stdin;
\.


--
-- Data for Name: payment_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payment_items (payment_id, item_id) FROM stdin;
\.


--
-- Data for Name: payment_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payment_plans (payment_id, plan_id) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payments (id, amount, guid, date, method, status, details, user_id) FROM stdin;
\.


--
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.plans (id, name, price, total_offers) FROM stdin;
\.


--
-- Data for Name: product_events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.product_events (product_id, event_id, discount) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.products (id, name, quantity, review, details, category_id, manufacture_id, advertisement_id, images) FROM stdin;
1	آیفون x	10	گوشی زیبای آیفون\r\n	\N	1	2	\N	[]
2	آیپاد new	12		\N	4	2	\N	['ad2.jpg', 'ad1.jpg']
\.


--
-- Data for Name: revoked_tokens; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.revoked_tokens (id, jti) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.roles (id, name, description) FROM stdin;
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.shipments (id, company, method, send_date, recieve_date, price, vehicle, status, insurance_id) FROM stdin;
\.


--
-- Data for Name: user_auction_likes; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_likes (user_id, auction_id, date) FROM stdin;
\.


--
-- Data for Name: user_auction_views; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_views (user_id, auction_id, count, ip, date) FROM stdin;
2	4	\N	\N	2018-05-08 23:02:40.008042
\.


--
-- Data for Name: user_auctions; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auctions (auction_id, user_id, date) FROM stdin;
4	1	2018-05-08 23:02:40.039717
4	2	2018-05-08 23:02:40.039732
\.


--
-- Data for Name: user_gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_gifts (user_id, gift_id, used) FROM stdin;
\.


--
-- Data for Name: user_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_plans (user_id, plan_id, used) FROM stdin;
\.


--
-- Data for Name: user_product_likes; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_product_likes (product_id, user_id) FROM stdin;
\.


--
-- Data for Name: user_product_views; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_product_views (product_id, user_id, ip_address, date) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_roles (role_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.users (id, username, first_name, last_name, work_place, mobile, email, password, avatar, created_at, updated_at, invitor, credit, address_id) FROM stdin;
1	mr_asadi	\N	\N	\N	09360284814	\N	$pbkdf2-sha256$29000$.n.PsXauFcI4J8T4X0tpTQ$0rGRxiCYB2mC8BXOsAaxzGma23QzH5bYzfgBzGQDOfk	\N	2018-05-06 09:10:49	2018-05-06 09:10:49	\N	0.0000	\N
2	SMRF	\N	\N	\N	123	\N	$pbkdf2-sha256$29000$Q8gZQ8j5/39P6d0b4/zfuw$KxzlvgayjDZg646AWABTWqOwdYTUcuQjcWZz3V4ShFU	\N	2018-05-07 17:08:15	2018-05-07 17:08:15	\N	0.0000	\N
\.


--
-- Name: addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.addresses_id_seq', 1, false);


--
-- Name: advertisements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.advertisements_id_seq', 4, true);


--
-- Name: auctions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.auctions_id_seq', 5, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.events_id_seq', 2, true);


--
-- Name: gifts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.gifts_id_seq', 1, false);


--
-- Name: insurances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.insurances_id_seq', 2, true);


--
-- Name: inventories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.inventories_id_seq', 2, true);


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.items_id_seq', 4, true);


--
-- Name: manufactures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.manufactures_id_seq', 2, true);


--
-- Name: offer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.offer_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.plans_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.products_id_seq', 6, true);


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.revoked_tokens_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- Name: shipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.shipments_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


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
-- Name: gifts gifts_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT gifts_pkey PRIMARY KEY (id);


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
-- Name: offer offer_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


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
-- Name: revoked_tokens revoked_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.revoked_tokens
    ADD CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (id);


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
-- Name: advertisements advertisements_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.advertisements
    ADD CONSTRAINT advertisements_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: auction_events auction_events_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_events
    ADD CONSTRAINT auction_events_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: auction_events auction_events_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_events
    ADD CONSTRAINT auction_events_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


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
-- Name: insurance_items insurance_items_insurance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurance_items
    ADD CONSTRAINT insurance_items_insurance_id_fkey FOREIGN KEY (insurance_id) REFERENCES public.insurances(id);


--
-- Name: insurance_items insurance_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurance_items
    ADD CONSTRAINT insurance_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: inventories inventories_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventories
    ADD CONSTRAINT inventories_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: inventory_items inventory_items_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_items
    ADD CONSTRAINT inventory_items_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventories(id);


--
-- Name: inventory_items inventory_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_items
    ADD CONSTRAINT inventory_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: items items_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventories(id);


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
-- Name: offer offer_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: offer offer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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
-- Name: orders orders_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payment_items payment_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_items
    ADD CONSTRAINT payment_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: payment_items payment_items_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_items
    ADD CONSTRAINT payment_items_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: payment_plans payment_plans_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_plans
    ADD CONSTRAINT payment_plans_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: payment_plans payment_plans_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_plans
    ADD CONSTRAINT payment_plans_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: product_events product_events_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.product_events
    ADD CONSTRAINT product_events_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: product_events product_events_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.product_events
    ADD CONSTRAINT product_events_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


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
-- Name: user_auctions user_auctions_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auctions
    ADD CONSTRAINT user_auctions_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_auctions user_auctions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auctions
    ADD CONSTRAINT user_auctions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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
-- Name: user_plans user_plans_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id);


--
-- Name: user_plans user_plans_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_product_likes user_product_likes_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_likes
    ADD CONSTRAINT user_product_likes_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: user_product_likes user_product_likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_likes
    ADD CONSTRAINT user_product_likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_product_views user_product_views_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_views
    ADD CONSTRAINT user_product_views_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: user_product_views user_product_views_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_views
    ADD CONSTRAINT user_product_views_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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
    country character varying(50),
    state character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    address character varying(255) NOT NULL,
    postal_code character varying(20) NOT NULL
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
    description character varying(100) NOT NULL,
    link_title character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    auction_id bigint,
    show boolean DEFAULT false,
    product_id bigint,
    images text
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
-- Name: auction_events; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auction_events (
    auction_id bigint,
    event_id bigint,
    discount numeric(20,4)
);


ALTER TABLE public.auction_events OWNER TO bidbazi;

--
-- Name: auctions; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.auctions (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    register_price numeric(20,4) NOT NULL,
    minimum_price numeric(20,4) NOT NULL,
    maximum_price numeric(20,4) NOT NULL,
    max_members bigint,
    item_id bigint,
    rate integer DEFAULT 1
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
    name character varying(100) NOT NULL,
    description character varying(255),
    category_id bigint,
    icon text
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
    message character varying(2048) NOT NULL,
    likes integer,
    date timestamp without time zone NOT NULL,
    user_id bigint,
    product_id bigint
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
    title character varying(255),
    description text,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    active boolean DEFAULT false,
    discount integer DEFAULT 0
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
-- Name: gifts; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.gifts (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    amount numeric(20,4)
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
-- Name: insurance_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.insurance_items (
    insurance_id bigint,
    item_id bigint
);


ALTER TABLE public.insurance_items OWNER TO bidbazi;

--
-- Name: insurances; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.insurances (
    id bigint NOT NULL,
    company_name character varying(100) NOT NULL,
    description text,
    price numeric(20,4) NOT NULL
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
    desciption character varying(255),
    address_id bigint
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
-- Name: inventory_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.inventory_items (
    inventory_id bigint,
    item_id bigint,
    count integer
);


ALTER TABLE public.inventory_items OWNER TO bidbazi;

--
-- Name: items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.items (
    id bigint NOT NULL,
    model character varying(100) NOT NULL,
    description text,
    price numeric(20,4) NOT NULL,
    product_id bigint,
    inventory_id bigint,
    discount integer DEFAULT 0
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
    review text,
    details bytea
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
-- Name: offer; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.offer (
    id bigint NOT NULL,
    offer_price numeric(20,4) NOT NULL,
    date timestamp without time zone,
    status integer,
    win boolean,
    user_id bigint,
    item_id bigint
);


ALTER TABLE public.offer OWNER TO bidbazi;

--
-- Name: offer_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.offer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.offer_id_seq OWNER TO bidbazi;

--
-- Name: offer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.offer_id_seq OWNED BY public.offer.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.order_items (
    item_id bigint,
    order_id bigint
);


ALTER TABLE public.order_items OWNER TO bidbazi;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    create_at timestamp without time zone,
    updated_at timestamp without time zone,
    status boolean,
    user_id bigint,
    shipment_id bigint
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
-- Name: payment_items; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payment_items (
    payment_id integer,
    item_id bigint
);


ALTER TABLE public.payment_items OWNER TO bidbazi;

--
-- Name: payment_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payment_plans (
    payment_id integer,
    plan_id bigint
);


ALTER TABLE public.payment_plans OWNER TO bidbazi;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    amount numeric(20,4) NOT NULL,
    guid character varying(50),
    date timestamp without time zone,
    method bytea,
    status boolean,
    details bytea,
    user_id bigint
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
    name character varying(100) NOT NULL,
    price numeric(20,4),
    total_offers integer
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
-- Name: product_events; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.product_events (
    product_id bigint,
    event_id bigint,
    discount numeric(20,4)
);


ALTER TABLE public.product_events OWNER TO bidbazi;

--
-- Name: products; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.products (
    id bigint NOT NULL,
    name character varying(25) NOT NULL,
    quantity integer NOT NULL,
    review text,
    details bytea,
    category_id bigint,
    manufacture_id bigint,
    advertisement_id bigint,
    images text
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
-- Name: revoked_tokens; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.revoked_tokens (
    id integer NOT NULL,
    jti character varying(120)
);


ALTER TABLE public.revoked_tokens OWNER TO bidbazi;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: bidbazi
--

CREATE SEQUENCE public.revoked_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.revoked_tokens_id_seq OWNER TO bidbazi;

--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bidbazi
--

ALTER SEQUENCE public.revoked_tokens_id_seq OWNED BY public.revoked_tokens.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.roles (
    id bigint NOT NULL,
    name character varying(80) NOT NULL,
    description character varying(512)
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
-- Name: shipments; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.shipments (
    id bigint NOT NULL,
    company character varying(100) NOT NULL,
    method character varying(100) NOT NULL,
    send_date timestamp without time zone,
    recieve_date timestamp without time zone,
    price numeric(20,4) NOT NULL,
    vehicle character varying(35),
    status boolean,
    insurance_id bigint
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
-- Name: user_auctions; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_auctions (
    auction_id bigint,
    user_id bigint,
    date timestamp without time zone
);


ALTER TABLE public.user_auctions OWNER TO bidbazi;

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
-- Name: user_plans; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_plans (
    user_id bigint,
    plan_id bigint,
    used boolean
);


ALTER TABLE public.user_plans OWNER TO bidbazi;

--
-- Name: user_product_likes; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_product_likes (
    product_id bigint,
    user_id bigint
);


ALTER TABLE public.user_product_likes OWNER TO bidbazi;

--
-- Name: user_product_views; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_product_views (
    product_id bigint,
    user_id bigint,
    ip_address character varying(64),
    date timestamp without time zone
);


ALTER TABLE public.user_product_views OWNER TO bidbazi;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: bidbazi
--

CREATE TABLE public.user_roles (
    role_id bigint,
    user_id bigint
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
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    invitor character varying(255),
    credit numeric(20,4),
    address_id bigint
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
-- Name: gifts id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts ALTER COLUMN id SET DEFAULT nextval('public.gifts_id_seq'::regclass);


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
-- Name: offer id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer ALTER COLUMN id SET DEFAULT nextval('public.offer_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


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
-- Name: revoked_tokens id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.revoked_tokens ALTER COLUMN id SET DEFAULT nextval('public.revoked_tokens_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: shipments id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments ALTER COLUMN id SET DEFAULT nextval('public.shipments_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.addresses (id, country, state, city, address, postal_code) FROM stdin;
\.


--
-- Data for Name: advertisements; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.advertisements (id, title, description, link_title, created_at, updated_at, auction_id, show, product_id, images) FROM stdin;
3	آی پد	این یک آی پد زیباست	برای یک خرید خوب کلیک کنید شوید	2018-05-06 20:42:55	2018-05-06 20:42:55	4	t	2	['slide3.jpg']
2	تبلیغ جدید	این یک تبلیغ جدید است	شانس خود را امتحان کنید	2018-05-06 19:36:00	2018-05-06 19:36:00	\N	t	1	['slide2.png']
4	تبلیغات حراجی زیبا	اینا همش حرفه	بپر تو..!	2018-05-09 05:00:34	2018-05-18 05:00:34	\N	t	1	['ad1.jpg']
\.


--
-- Data for Name: auction_events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auction_events (auction_id, event_id, discount) FROM stdin;
4	1	\N
4	2	\N
\.


--
-- Data for Name: auctions; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.auctions (id, name, description, created_at, updated_at, start_date, end_date, register_price, minimum_price, maximum_price, max_members, item_id, rate) FROM stdin;
3	حراجی آيفون ایکس	این یک حراجی فوق العاده است	2018-05-07 16:37:42	2018-05-07 16:37:42	2018-05-07 16:37:42	2018-05-09 16:37:42	150000.0000	10000.0000	200000.0000	40	3	1
4	test	test	2018-05-08 10:50:55	2018-05-08 10:50:55	2018-05-07 10:50:55	2018-05-10 18:50:00	3424.0000	43.0000	2.0000	40	4	1
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.categories (id, name, description, category_id, icon) FROM stdin;
4	تبلت	این دسته بندی مربوط به تبلت است	\N	['for3_2.png']
2	لوازم خانگی	این دسته بندی مربوط به لوازم خانگی است	\N	['for2_2.png']
3	موبایل	این دسته بندی مربوط به موبایل است	\N	['for3_2.png']
1	دیجتال	این دسته بندی لوازم دیجیتالی است	\N	['arrow-down.png']
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.comments (id, title, message, likes, date, user_id, product_id) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.events (id, title, description, start_date, end_date, active, discount) FROM stdin;
2	حراجی محصولات سایت 	تخفیف در دسته بندی لوازم خانگی! 	2018-05-07 13:54:30	2018-05-07 15:54:00	t	40
1	به مناسبت افتتاح سایت	تخفیف در حراجی های طلایی!	2018-05-07 11:47:43	2018-05-12 11:47:43	t	20
\.


--
-- Data for Name: gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.gifts (id, name, amount) FROM stdin;
\.


--
-- Data for Name: insurance_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.insurance_items (insurance_id, item_id) FROM stdin;
2	3
\.


--
-- Data for Name: insurances; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.insurances (id, company_name, description, price) FROM stdin;
1	گارانتی سازگار		12000.0000
2	گارانتی پارامیس		30000.0000
\.


--
-- Data for Name: inventories; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventories (id, name, desciption, address_id) FROM stdin;
1	شرکت	انبار مرکزی شرکت	\N
2	ولیعصر	بازارچه رضا - مغازه ۵	\N
\.


--
-- Data for Name: inventory_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.inventory_items (inventory_id, item_id, count) FROM stdin;
2	3	\N
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.items (id, model, description, price, product_id, inventory_id, discount) FROM stdin;
4	جدیدترین مدل	این یک آیپد جدید است	4300000.0000	2	\N	30
3	۱۲۸ گیگابایت	این یک آیتم از گوشی های زیبای آیفون است	2500000.0000	1	\N	25
\.


--
-- Data for Name: manufacture_products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufacture_products (manufacture_id, product_id) FROM stdin;
\.


--
-- Data for Name: manufactures; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.manufactures (id, name, country, review, details) FROM stdin;
1	سامسونگ	کره	این توضیحات مربوط به کارخانه سامسونگ است	\N
2	اپل	آمریکا	\r\n	\N
\.


--
-- Data for Name: offer; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.offer (id, offer_price, date, status, win, user_id, item_id) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.order_items (item_id, order_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.orders (id, create_at, updated_at, status, user_id, shipment_id) FROM stdin;
\.


--
-- Data for Name: payment_items; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payment_items (payment_id, item_id) FROM stdin;
\.


--
-- Data for Name: payment_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payment_plans (payment_id, plan_id) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.payments (id, amount, guid, date, method, status, details, user_id) FROM stdin;
\.


--
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.plans (id, name, price, total_offers) FROM stdin;
\.


--
-- Data for Name: product_events; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.product_events (product_id, event_id, discount) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.products (id, name, quantity, review, details, category_id, manufacture_id, advertisement_id, images) FROM stdin;
2	آیپاد new	12		\N	4	2	\N	['2.jpg']
1	آیفون x	10	گوشی زیبای آیفون\r\n	\N	1	2	\N	['2.jpg', '3.jpg', '1.jpg']
\.


--
-- Data for Name: revoked_tokens; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.revoked_tokens (id, jti) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.roles (id, name, description) FROM stdin;
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.shipments (id, company, method, send_date, recieve_date, price, vehicle, status, insurance_id) FROM stdin;
\.


--
-- Data for Name: user_auction_likes; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_likes (user_id, auction_id, date) FROM stdin;
1	3	2018-05-09 18:03:38.779332
\.


--
-- Data for Name: user_auction_views; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auction_views (user_id, auction_id, count, ip, date) FROM stdin;
2	4	\N	\N	2018-05-08 23:02:40.008042
\.


--
-- Data for Name: user_auctions; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_auctions (auction_id, user_id, date) FROM stdin;
4	1	2018-05-08 23:02:40.039717
4	2	2018-05-08 23:02:40.039732
\.


--
-- Data for Name: user_gifts; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_gifts (user_id, gift_id, used) FROM stdin;
\.


--
-- Data for Name: user_plans; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_plans (user_id, plan_id, used) FROM stdin;
\.


--
-- Data for Name: user_product_likes; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_product_likes (product_id, user_id) FROM stdin;
1	2
2	2
1	1
\.


--
-- Data for Name: user_product_views; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_product_views (product_id, user_id, ip_address, date) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.user_roles (role_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bidbazi
--

COPY public.users (id, username, first_name, last_name, work_place, mobile, email, password, avatar, created_at, updated_at, invitor, credit, address_id) FROM stdin;
1	mr_asadi	محمدرضا	اسدی	شیراز	09360284814	\N	$pbkdf2-sha256$29000$.n.PsXauFcI4J8T4X0tpTQ$0rGRxiCYB2mC8BXOsAaxzGma23QzH5bYzfgBzGQDOfk	['005.png']	2018-05-06 09:10:49	2018-05-06 09:10:49	\N	0.0000	\N
2	SMRF	محمدرضا	فرزانمهر	\N	123	\N	$pbkdf2-sha256$29000$Q8gZQ8j5/39P6d0b4/zfuw$KxzlvgayjDZg646AWABTWqOwdYTUcuQjcWZz3V4ShFU	['004.png']	2018-05-07 17:08:15	2018-05-07 17:08:15	\N	0.0000	\N
\.


--
-- Name: addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.addresses_id_seq', 1, false);


--
-- Name: advertisements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.advertisements_id_seq', 4, true);


--
-- Name: auctions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.auctions_id_seq', 5, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.events_id_seq', 2, true);


--
-- Name: gifts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.gifts_id_seq', 1, false);


--
-- Name: insurances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.insurances_id_seq', 2, true);


--
-- Name: inventories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.inventories_id_seq', 2, true);


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.items_id_seq', 4, true);


--
-- Name: manufactures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.manufactures_id_seq', 2, true);


--
-- Name: offer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.offer_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.plans_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.products_id_seq', 6, true);


--
-- Name: revoked_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.revoked_tokens_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- Name: shipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.shipments_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bidbazi
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


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
-- Name: gifts gifts_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT gifts_pkey PRIMARY KEY (id);


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
-- Name: offer offer_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


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
-- Name: revoked_tokens revoked_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.revoked_tokens
    ADD CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (id);


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
-- Name: advertisements advertisements_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.advertisements
    ADD CONSTRAINT advertisements_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: auction_events auction_events_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_events
    ADD CONSTRAINT auction_events_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: auction_events auction_events_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.auction_events
    ADD CONSTRAINT auction_events_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


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
-- Name: insurance_items insurance_items_insurance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurance_items
    ADD CONSTRAINT insurance_items_insurance_id_fkey FOREIGN KEY (insurance_id) REFERENCES public.insurances(id);


--
-- Name: insurance_items insurance_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.insurance_items
    ADD CONSTRAINT insurance_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: inventories inventories_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventories
    ADD CONSTRAINT inventories_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: inventory_items inventory_items_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_items
    ADD CONSTRAINT inventory_items_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventories(id);


--
-- Name: inventory_items inventory_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.inventory_items
    ADD CONSTRAINT inventory_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: items items_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_inventory_id_fkey FOREIGN KEY (inventory_id) REFERENCES public.inventories(id);


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
-- Name: offer offer_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: offer offer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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
-- Name: orders orders_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payment_items payment_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_items
    ADD CONSTRAINT payment_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: payment_items payment_items_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_items
    ADD CONSTRAINT payment_items_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: payment_plans payment_plans_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_plans
    ADD CONSTRAINT payment_plans_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: payment_plans payment_plans_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payment_plans
    ADD CONSTRAINT payment_plans_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: product_events product_events_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.product_events
    ADD CONSTRAINT product_events_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: product_events product_events_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.product_events
    ADD CONSTRAINT product_events_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


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
-- Name: user_auctions user_auctions_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auctions
    ADD CONSTRAINT user_auctions_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id);


--
-- Name: user_auctions user_auctions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_auctions
    ADD CONSTRAINT user_auctions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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
-- Name: user_plans user_plans_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.plans(id);


--
-- Name: user_plans user_plans_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_plans
    ADD CONSTRAINT user_plans_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_product_likes user_product_likes_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_likes
    ADD CONSTRAINT user_product_likes_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: user_product_likes user_product_likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_likes
    ADD CONSTRAINT user_product_likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_product_views user_product_views_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_views
    ADD CONSTRAINT user_product_views_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: user_product_views user_product_views_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bidbazi
--

ALTER TABLE ONLY public.user_product_views
    ADD CONSTRAINT user_product_views_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


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

