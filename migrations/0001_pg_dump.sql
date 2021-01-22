--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: currency; Type: TABLE; Schema: public; Owner: bravo
--

CREATE TABLE public.currency (
    id integer NOT NULL,
    code character varying(4) NOT NULL,
    value double precision NOT NULL,
    active boolean NOT NULL,
    last_update date NOT NULL
);


ALTER TABLE public.currency OWNER TO bravo;

--
-- Name: currency_id_seq; Type: SEQUENCE; Schema: public; Owner: bravo
--

CREATE SEQUENCE public.currency_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.currency_id_seq OWNER TO bravo;

--
-- Name: currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bravo
--

ALTER SEQUENCE public.currency_id_seq OWNED BY public.currency.id;


--
-- Name: currency id; Type: DEFAULT; Schema: public; Owner: bravo
--

ALTER TABLE ONLY public.currency ALTER COLUMN id SET DEFAULT nextval('public.currency_id_seq'::regclass);


--
-- Data for Name: currency; Type: TABLE DATA; Schema: public; Owner: bravo
--

COPY public.currency (id, code, value, active, last_update) FROM stdin;
\.


--
-- Name: currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bravo
--

SELECT pg_catalog.setval('public.currency_id_seq', 1, false);


--
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: public; Owner: bravo
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (id);



GRANT ALL PRIVILEGES ON DATABASE bravo TO bravo;
