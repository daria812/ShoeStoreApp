--
-- PostgreSQL database dump
--

\restrict ji0iF9pkTGtoKgQnNbKxz2eJtS4CPBRWdeS7UmD1Z26OyDQIWcmVEobWvudhcIW

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-04-21 18:07:21

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 16425)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16424)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- TOC entry 5148 (class 0 OID 0)
-- Dependencies: 229
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 245 (class 1259 OID 16570)
-- Name: import_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.import_users (
    role character varying(30),
    full_name character varying(150),
    login character varying(100),
    password character varying(50)
);


ALTER TABLE public.import_users OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16436)
-- Name: manufacturers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.manufacturers (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.manufacturers OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16435)
-- Name: manufacturers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.manufacturers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.manufacturers_id_seq OWNER TO postgres;

--
-- TOC entry 5149 (class 0 OID 0)
-- Dependencies: 231
-- Name: manufacturers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.manufacturers_id_seq OWNED BY public.manufacturers.id;


--
-- TOC entry 242 (class 1259 OID 16532)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer NOT NULL,
    price_at_moment numeric(10,2)
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16531)
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- TOC entry 5150 (class 0 OID 0)
-- Dependencies: 241
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- TOC entry 228 (class 1259 OID 16414)
-- Name: order_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_statuses (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.order_statuses OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16413)
-- Name: order_statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_statuses_id_seq OWNER TO postgres;

--
-- TOC entry 5151 (class 0 OID 0)
-- Dependencies: 227
-- Name: order_statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_statuses_id_seq OWNED BY public.order_statuses.id;


--
-- TOC entry 240 (class 1259 OID 16507)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    order_number integer,
    user_id integer,
    order_status_id integer,
    order_date date,
    delivery_date date,
    pickup_point_id integer,
    pickup_code character varying(20)
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16506)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 5152 (class 0 OID 0)
-- Dependencies: 239
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 226 (class 1259 OID 16403)
-- Name: pickup_points; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pickup_points (
    id integer NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.pickup_points OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16402)
-- Name: pickup_points_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pickup_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pickup_points_id_seq OWNER TO postgres;

--
-- TOC entry 5153 (class 0 OID 0)
-- Dependencies: 225
-- Name: pickup_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pickup_points_id_seq OWNED BY public.pickup_points.id;


--
-- TOC entry 238 (class 1259 OID 16469)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    article character varying(50) NOT NULL,
    name character varying(200) NOT NULL,
    description text,
    category_id integer,
    manufacturer_id integer,
    supplier_id integer,
    unit_id integer,
    price numeric(10,2) NOT NULL,
    discount_percent numeric(5,2) DEFAULT 0,
    quantity_in_stock integer DEFAULT 0,
    image_path character varying(255),
    CONSTRAINT products_price_check CHECK ((price >= (0)::numeric))
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16468)
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- TOC entry 5154 (class 0 OID 0)
-- Dependencies: 237
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- TOC entry 234 (class 1259 OID 16447)
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16446)
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.suppliers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.suppliers_id_seq OWNER TO postgres;

--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 233
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- TOC entry 236 (class 1259 OID 16458)
-- Name: units; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.units (
    id integer NOT NULL,
    name character varying(20) NOT NULL
);


ALTER TABLE public.units OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16457)
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.units_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.units_id_seq OWNER TO postgres;

--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 235
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.units_id_seq OWNED BY public.units.id;


--
-- TOC entry 224 (class 1259 OID 16390)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying(100) NOT NULL,
    password_hash character varying(50) NOT NULL,
    role character varying(30) NOT NULL,
    full_name character varying(150)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16389)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4918 (class 2604 OID 16428)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 16439)
-- Name: manufacturers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturers ALTER COLUMN id SET DEFAULT nextval('public.manufacturers_id_seq'::regclass);


--
-- TOC entry 4926 (class 2604 OID 16535)
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- TOC entry 4917 (class 2604 OID 16417)
-- Name: order_statuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_statuses ALTER COLUMN id SET DEFAULT nextval('public.order_statuses_id_seq'::regclass);


--
-- TOC entry 4925 (class 2604 OID 16510)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 16406)
-- Name: pickup_points id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points ALTER COLUMN id SET DEFAULT nextval('public.pickup_points_id_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 16472)
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- TOC entry 4920 (class 2604 OID 16450)
-- Name: suppliers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- TOC entry 4921 (class 2604 OID 16461)
-- Name: units id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units ALTER COLUMN id SET DEFAULT nextval('public.units_id_seq'::regclass);


--
-- TOC entry 4915 (class 2604 OID 16393)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5129 (class 0 OID 16425)
-- Dependencies: 230
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories VALUES (1, 'Женская обувь');
INSERT INTO public.categories VALUES (2, 'Мужская обувь');


--
-- TOC entry 5142 (class 0 OID 16570)
-- Dependencies: 245
-- Data for Name: import_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.import_users VALUES ('Администратор', 'Никифорова Весения Николаевна', '94d5ous@gmail.com', 'uzWC67');
INSERT INTO public.import_users VALUES ('Администратор', 'Сазонов Руслан Германович', 'uth4iz@mail.com', '2L6KZG');
INSERT INTO public.import_users VALUES ('Администратор', 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ');
INSERT INTO public.import_users VALUES ('Менеджер', 'Степанов Михаил Артёмович', '1diph5e@tutanota.com', '8ntwUp');
INSERT INTO public.import_users VALUES ('Менеджер', 'Ворсин Петр Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR');
INSERT INTO public.import_users VALUES ('Менеджер', 'Старикова Елена Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv');
INSERT INTO public.import_users VALUES ('Авторизированный клиент', 'Михайлюк Анна Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9');
INSERT INTO public.import_users VALUES ('Авторизированный клиент', 'Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos');
INSERT INTO public.import_users VALUES ('Авторизированный клиент', 'Ворсин Петр Евгеньевич', '1qz4kw@mail.com', 'gynQMT');
INSERT INTO public.import_users VALUES ('Авторизированный клиент', 'Старикова Елена Павловна', '4np6se@mail.com', 'AtnDjr');


--
-- TOC entry 5131 (class 0 OID 16436)
-- Dependencies: 232
-- Data for Name: manufacturers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.manufacturers VALUES (1, 'Рос');
INSERT INTO public.manufacturers VALUES (2, 'Marco Tozzi');
INSERT INTO public.manufacturers VALUES (3, 'Rieker');
INSERT INTO public.manufacturers VALUES (4, 'CROSBY');
INSERT INTO public.manufacturers VALUES (5, 'Alessio Nesca');
INSERT INTO public.manufacturers VALUES (6, 'Kari');


--
-- TOC entry 5141 (class 0 OID 16532)
-- Dependencies: 242
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_items VALUES (1, 7, 42, 2, 4990.00);
INSERT INTO public.order_items VALUES (2, 7, 49, 2, 3244.00);
INSERT INTO public.order_items VALUES (3, 6, 40, 1, 4499.00);
INSERT INTO public.order_items VALUES (4, 6, 32, 1, 5900.00);
INSERT INTO public.order_items VALUES (5, 5, 50, 10, 3800.00);
INSERT INTO public.order_items VALUES (6, 5, 48, 10, 4100.00);
INSERT INTO public.order_items VALUES (7, 4, 33, 5, 2700.00);
INSERT INTO public.order_items VALUES (8, 4, 61, 4, 1890.00);
INSERT INTO public.order_items VALUES (9, 3, 42, 2, 4990.00);
INSERT INTO public.order_items VALUES (10, 3, 49, 2, 3244.00);
INSERT INTO public.order_items VALUES (11, 2, 40, 1, 4499.00);
INSERT INTO public.order_items VALUES (12, 2, 32, 1, 5900.00);
INSERT INTO public.order_items VALUES (13, 1, 50, 10, 3800.00);
INSERT INTO public.order_items VALUES (14, 1, 48, 10, 4100.00);
INSERT INTO public.order_items VALUES (15, 10, 33, 5, 2700.00);
INSERT INTO public.order_items VALUES (16, 10, 61, 4, 1890.00);
INSERT INTO public.order_items VALUES (17, 9, 35, 5, 4300.00);
INSERT INTO public.order_items VALUES (18, 9, 43, 1, 2800.00);
INSERT INTO public.order_items VALUES (19, 8, 57, 5, 2156.00);
INSERT INTO public.order_items VALUES (20, 8, 44, 5, 1800.00);


--
-- TOC entry 5127 (class 0 OID 16414)
-- Dependencies: 228
-- Data for Name: order_statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_statuses VALUES (1, 'Завершен');
INSERT INTO public.order_statuses VALUES (2, 'Новый');


--
-- TOC entry 5139 (class 0 OID 16507)
-- Dependencies: 240
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.orders VALUES (1, 7, 2, 1, '2025-02-28', '2025-04-26', 3, '907');
INSERT INTO public.orders VALUES (2, 6, 1, 1, '2025-03-01', '2025-04-25', 15, '906');
INSERT INTO public.orders VALUES (3, 5, 4, 1, '2025-03-17', '2025-04-24', 2, '905');
INSERT INTO public.orders VALUES (4, 4, 3, 1, '2025-02-20', '2025-04-23', 11, '904');
INSERT INTO public.orders VALUES (5, 3, 2, 1, '2025-03-21', '2025-04-22', 2, '903');
INSERT INTO public.orders VALUES (6, 2, 1, 1, '2022-09-28', '2025-04-21', 11, '902');
INSERT INTO public.orders VALUES (7, 1, 4, 1, '2025-02-27', '2025-04-20', 1, '901');
INSERT INTO public.orders VALUES (8, 10, 4, 2, '2025-04-03', '2025-04-29', 19, '910');
INSERT INTO public.orders VALUES (9, 9, 4, 2, '2025-04-02', '2025-04-28', 5, '909');
INSERT INTO public.orders VALUES (10, 8, 3, 2, '2025-03-31', '2025-04-27', 19, '908');


--
-- TOC entry 5125 (class 0 OID 16403)
-- Dependencies: 226
-- Data for Name: pickup_points; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.pickup_points VALUES (1, '420151, г. Лесной, ул. Вишневая, 32');
INSERT INTO public.pickup_points VALUES (2, '125061, г. Лесной, ул. Подгорная, 8');
INSERT INTO public.pickup_points VALUES (3, '630370, г. Лесной, ул. Шоссейная, 24');
INSERT INTO public.pickup_points VALUES (4, '400562, г. Лесной, ул. Зеленая, 32');
INSERT INTO public.pickup_points VALUES (5, '614510, г. Лесной, ул. Маяковского, 47');
INSERT INTO public.pickup_points VALUES (6, '410542, г. Лесной, ул. Светлая, 46');
INSERT INTO public.pickup_points VALUES (7, '620839, г. Лесной, ул. Цветочная, 8');
INSERT INTO public.pickup_points VALUES (8, '443890, г. Лесной, ул. Коммунистическая, 1');
INSERT INTO public.pickup_points VALUES (9, '603379, г. Лесной, ул. Спортивная, 46');
INSERT INTO public.pickup_points VALUES (10, '603721, г. Лесной, ул. Гоголя, 41');
INSERT INTO public.pickup_points VALUES (11, '410172, г. Лесной, ул. Северная, 13');
INSERT INTO public.pickup_points VALUES (12, '614611, г. Лесной, ул. Молодежная, 50');
INSERT INTO public.pickup_points VALUES (13, '454311, г.Лесной, ул. Новая, 19');
INSERT INTO public.pickup_points VALUES (14, '660007, г.Лесной, ул. Октябрьская, 19');
INSERT INTO public.pickup_points VALUES (15, '603036, г. Лесной, ул. Садовая, 4');
INSERT INTO public.pickup_points VALUES (16, '394060, г.Лесной, ул. Фрунзе, 43');
INSERT INTO public.pickup_points VALUES (17, '410661, г. Лесной, ул. Школьная, 50');
INSERT INTO public.pickup_points VALUES (18, '625590, г. Лесной, ул. Коммунистическая, 20');
INSERT INTO public.pickup_points VALUES (19, '625683, г. Лесной, ул. 8 Марта');
INSERT INTO public.pickup_points VALUES (20, '450983, г.Лесной, ул. Комсомольская, 26');
INSERT INTO public.pickup_points VALUES (21, '394782, г. Лесной, ул. Чехова, 3');
INSERT INTO public.pickup_points VALUES (22, '603002, г. Лесной, ул. Дзержинского, 28');
INSERT INTO public.pickup_points VALUES (23, '450558, г. Лесной, ул. Набережная, 30');
INSERT INTO public.pickup_points VALUES (24, '344288, г. Лесной, ул. Чехова, 1');
INSERT INTO public.pickup_points VALUES (25, '614164, г.Лесной,  ул. Степная, 30');
INSERT INTO public.pickup_points VALUES (26, '394242, г. Лесной, ул. Коммунистическая, 43');
INSERT INTO public.pickup_points VALUES (27, '660540, г. Лесной, ул. Солнечная, 25');
INSERT INTO public.pickup_points VALUES (28, '125837, г. Лесной, ул. Шоссейная, 40');
INSERT INTO public.pickup_points VALUES (29, '125703, г. Лесной, ул. Партизанская, 49');
INSERT INTO public.pickup_points VALUES (30, '625283, г. Лесной, ул. Победы, 46');
INSERT INTO public.pickup_points VALUES (31, '614753, г. Лесной, ул. Полевая, 35');
INSERT INTO public.pickup_points VALUES (32, '426030, г. Лесной, ул. Маяковского, 44');
INSERT INTO public.pickup_points VALUES (33, '450375, г. Лесной ул. Клубная, 44');
INSERT INTO public.pickup_points VALUES (34, '625560, г. Лесной, ул. Некрасова, 12');
INSERT INTO public.pickup_points VALUES (35, '630201, г. Лесной, ул. Комсомольская, 17');
INSERT INTO public.pickup_points VALUES (36, '190949, г. Лесной, ул. Мичурина, 26');


--
-- TOC entry 5137 (class 0 OID 16469)
-- Dependencies: 238
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products VALUES (32, 'G783F5', 'Ботинки', 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', 2, 1, 2, 1, 5900.00, 2.00, 8, 'images/4.jpg');
INSERT INTO public.products VALUES (33, 'F572H7', 'Туфли', 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', 1, 2, 2, 1, 2700.00, 2.00, 14, 'images/7.jpg');
INSERT INTO public.products VALUES (34, 'K358H6', 'Тапочки', 'Тапочки мужские син р.41', 2, 3, 2, 1, 599.00, 20.00, 2, NULL);
INSERT INTO public.products VALUES (35, 'B320R5', 'Туфли', 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', 1, 3, 2, 1, 4300.00, 2.00, 6, 'images/9.jpg');
INSERT INTO public.products VALUES (36, 'P764G4', 'Туфли', 'Туфли женские, ARGO, размер 38', 1, 4, 2, 1, 6800.00, 15.00, 15, NULL);
INSERT INTO public.products VALUES (37, 'N457T5', 'Полуботинки', 'Полуботинки Ботинки черные зимние, мех', 1, 4, 2, 1, 4600.00, 3.00, 13, NULL);
INSERT INTO public.products VALUES (38, 'T324F5', 'Сапоги', 'Сапоги замша Цвет: синий', 1, 4, 2, 1, 4699.00, 2.00, 5, NULL);
INSERT INTO public.products VALUES (39, 'C436G5', 'Ботинки', 'Ботинки женские, ARGO, размер 40', 1, 5, 2, 1, 10200.00, 15.00, 9, NULL);
INSERT INTO public.products VALUES (40, 'H782T5', 'Туфли', 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', 2, 6, 2, 1, 4499.00, 4.00, 5, 'images/3.jpg');
INSERT INTO public.products VALUES (41, 'J542F5', 'Тапочки', 'Тапочки мужские Арт.70701-55-67син р.41', 2, 6, 2, 1, 500.00, 13.00, 0, NULL);
INSERT INTO public.products VALUES (42, 'А112Т4', 'Ботинки', 'Женские Ботинки демисезонные kari', 1, 6, 2, 1, 4990.00, 3.00, 6, 'images/1.jpg');
INSERT INTO public.products VALUES (43, 'G432E4', 'Туфли', 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', 1, 6, 2, 1, 2800.00, 3.00, 15, 'images/10.jpg');
INSERT INTO public.products VALUES (44, 'E482R4', 'Полуботинки', 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', 1, 6, 2, 1, 1800.00, 2.00, 14, NULL);
INSERT INTO public.products VALUES (45, 'G531F4', 'Ботинки', 'Ботинки женские зимние ROMER арт. 893167-01 Черный', 1, 6, 2, 1, 6600.00, 12.00, 9, NULL);
INSERT INTO public.products VALUES (46, 'D364R4', 'Туфли', 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', 1, 6, 2, 1, 12400.00, 16.00, 5, NULL);
INSERT INTO public.products VALUES (47, 'L754R4', 'Полуботинки', 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', 1, 6, 2, 1, 1700.00, 2.00, 7, NULL);
INSERT INTO public.products VALUES (48, 'D572U8', 'Кроссовки', '129615-4 Кроссовки мужские', 2, 1, 1, 1, 4100.00, 3.00, 6, 'images/6.jpg');
INSERT INTO public.products VALUES (49, 'F635R4', 'Ботинки', 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', 1, 2, 1, 1, 3244.00, 2.00, 13, 'images/2.jpg');
INSERT INTO public.products VALUES (50, 'J384T6', 'Ботинки', 'B3430/14 Полуботинки мужские Rieker', 2, 3, 1, 1, 3800.00, 2.00, 16, 'images/5.jpg');
INSERT INTO public.products VALUES (51, 'B431R5', 'Ботинки', 'Мужские кожаные ботинки/мужские ботинки', 2, 3, 1, 1, 2700.00, 2.00, 5, NULL);
INSERT INTO public.products VALUES (52, 'M542T5', 'Кроссовки', 'Кроссовки мужские TOFA', 2, 3, 1, 1, 2800.00, 18.00, 3, NULL);
INSERT INTO public.products VALUES (53, 'O754F4', 'Туфли', 'Туфли женские демисезонные Rieker артикул 55073-68/37', 1, 3, 1, 1, 5400.00, 4.00, 18, NULL);
INSERT INTO public.products VALUES (54, 'F427R5', 'Ботинки', 'Ботинки на молнии с декоративной пряжкой FRAU', 1, 3, 1, 1, 11800.00, 15.00, 11, NULL);
INSERT INTO public.products VALUES (55, 'D268G5', 'Туфли', 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', 1, 3, 1, 1, 4399.00, 3.00, 12, NULL);
INSERT INTO public.products VALUES (56, 'H535R5', 'Ботинки', 'Женские Ботинки демисезонные', 1, 3, 1, 1, 2300.00, 2.00, 7, NULL);
INSERT INTO public.products VALUES (57, 'S213E3', 'Полуботинки', '407700/01-01 Полуботинки мужские CROSBY', 2, 4, 1, 1, 2156.00, 3.00, 6, NULL);
INSERT INTO public.products VALUES (58, 'S634B5', 'Кеды', 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', 2, 4, 1, 1, 5500.00, 3.00, 0, NULL);
INSERT INTO public.products VALUES (59, 'K345R4', 'Полуботинки', '407700/01-02 Полуботинки мужские CROSBY', 2, 4, 1, 1, 2100.00, 2.00, 3, NULL);
INSERT INTO public.products VALUES (60, 'S326R5', 'Тапочки', 'Мужские кожаные тапочки Профиль С.Дали ', 2, 4, 1, 1, 9900.00, 17.00, 15, NULL);
INSERT INTO public.products VALUES (61, 'D329H3', 'Полуботинки', 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', 1, 5, 1, 1, 1890.00, 4.00, 4, 'images/8.jpg');


--
-- TOC entry 5133 (class 0 OID 16447)
-- Dependencies: 234
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.suppliers VALUES (1, 'Обувь для вас');
INSERT INTO public.suppliers VALUES (2, 'Kari');


--
-- TOC entry 5135 (class 0 OID 16458)
-- Dependencies: 236
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.units VALUES (1, 'шт.');


--
-- TOC entry 5123 (class 0 OID 16390)
-- Dependencies: 224
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, '94d5ous@gmail.com', 'uzWC67', 'admin', 'Никифорова Весения Николаевна');
INSERT INTO public.users VALUES (2, 'uth4iz@mail.com', '2L6KZG', 'admin', 'Сазонов Руслан Германович');
INSERT INTO public.users VALUES (3, 'yzls62@outlook.com', 'JlFRCZ', 'admin', 'Одинцов Серафим Артёмович');
INSERT INTO public.users VALUES (4, '1diph5e@tutanota.com', '8ntwUp', 'manager', 'Степанов Михаил Артёмович');
INSERT INTO public.users VALUES (5, 'tjde7c@yahoo.com', 'YOyhfR', 'manager', 'Ворсин Петр Евгеньевич');
INSERT INTO public.users VALUES (6, 'wpmrc3do@tutanota.com', 'RSbvHv', 'manager', 'Старикова Елена Павловна');
INSERT INTO public.users VALUES (7, '5d4zbu@tutanota.com', 'rwVDh9', 'client', 'Михайлюк Анна Вячеславовна');
INSERT INTO public.users VALUES (8, 'ptec8ym@yahoo.com', 'LdNyos', 'client', 'Ситдикова Елена Анатольевна');
INSERT INTO public.users VALUES (9, '1qz4kw@mail.com', 'gynQMT', 'client', 'Ворсин Петр Евгеньевич');
INSERT INTO public.users VALUES (10, '4np6se@mail.com', 'AtnDjr', 'client', 'Старикова Елена Павловна');


--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 229
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 2, true);


--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 231
-- Name: manufacturers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.manufacturers_id_seq', 6, true);


--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 241
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 20, true);


--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 227
-- Name: order_statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_statuses_id_seq', 2, true);


--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 239
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 10, true);


--
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 225
-- Name: pickup_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pickup_points_id_seq', 36, true);


--
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 237
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 61, true);


--
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 233
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 2, true);


--
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 235
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.units_id_seq', 1, true);


--
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 4941 (class 2606 OID 16434)
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- TOC entry 4943 (class 2606 OID 16432)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 4945 (class 2606 OID 16445)
-- Name: manufacturers manufacturers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturers
    ADD CONSTRAINT manufacturers_name_key UNIQUE (name);


--
-- TOC entry 4947 (class 2606 OID 16443)
-- Name: manufacturers manufacturers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturers
    ADD CONSTRAINT manufacturers_pkey PRIMARY KEY (id);


--
-- TOC entry 4965 (class 2606 OID 16539)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 4937 (class 2606 OID 16423)
-- Name: order_statuses order_statuses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_statuses
    ADD CONSTRAINT order_statuses_name_key UNIQUE (name);


--
-- TOC entry 4939 (class 2606 OID 16421)
-- Name: order_statuses order_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_statuses
    ADD CONSTRAINT order_statuses_pkey PRIMARY KEY (id);


--
-- TOC entry 4961 (class 2606 OID 16515)
-- Name: orders orders_order_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_order_number_key UNIQUE (order_number);


--
-- TOC entry 4963 (class 2606 OID 16513)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4933 (class 2606 OID 16412)
-- Name: pickup_points pickup_points_address_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points
    ADD CONSTRAINT pickup_points_address_key UNIQUE (address);


--
-- TOC entry 4935 (class 2606 OID 16410)
-- Name: pickup_points pickup_points_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points
    ADD CONSTRAINT pickup_points_pkey PRIMARY KEY (id);


--
-- TOC entry 4957 (class 2606 OID 16485)
-- Name: products products_article_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_article_key UNIQUE (article);


--
-- TOC entry 4959 (class 2606 OID 16483)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- TOC entry 4949 (class 2606 OID 16456)
-- Name: suppliers suppliers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_name_key UNIQUE (name);


--
-- TOC entry 4951 (class 2606 OID 16454)
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- TOC entry 4953 (class 2606 OID 16467)
-- Name: units units_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_name_key UNIQUE (name);


--
-- TOC entry 4955 (class 2606 OID 16465)
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- TOC entry 4929 (class 2606 OID 16401)
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- TOC entry 4931 (class 2606 OID 16399)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4973 (class 2606 OID 16540)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 4974 (class 2606 OID 16545)
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- TOC entry 4970 (class 2606 OID 16521)
-- Name: orders orders_order_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_order_status_id_fkey FOREIGN KEY (order_status_id) REFERENCES public.order_statuses(id);


--
-- TOC entry 4971 (class 2606 OID 16526)
-- Name: orders orders_pickup_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pickup_point_id_fkey FOREIGN KEY (pickup_point_id) REFERENCES public.pickup_points(id);


--
-- TOC entry 4972 (class 2606 OID 16516)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4966 (class 2606 OID 16486)
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- TOC entry 4967 (class 2606 OID 16491)
-- Name: products products_manufacturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_manufacturer_id_fkey FOREIGN KEY (manufacturer_id) REFERENCES public.manufacturers(id);


--
-- TOC entry 4968 (class 2606 OID 16496)
-- Name: products products_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- TOC entry 4969 (class 2606 OID 16501)
-- Name: products products_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


-- Completed on 2026-04-21 18:07:22

--
-- PostgreSQL database dump complete
--

\unrestrict ji0iF9pkTGtoKgQnNbKxz2eJtS4CPBRWdeS7UmD1Z26OyDQIWcmVEobWvudhcIW

