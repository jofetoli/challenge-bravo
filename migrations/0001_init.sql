--
-- Name: currency; Type: TABLE; Schema: public; Owner: bravo
--

CREATE TABLE public.currency (
    id BIGSERIAL PRIMARY KEY,
    code character varying(4) NOT NULL,
    value double precision NOT NULL,
    active boolean NOT NULL,
    last_update date NOT NULL
);

ALTER TABLE public.currency OWNER TO bravo;

GRANT ALL PRIVILEGES ON DATABASE bravo TO bravo;
