from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


ABS_NORM_FUNC = """
CREATE OR REPLACE FUNCTION public.abs_norm(IN red_1 integer[], IN green_1 integer[], IN blue_1 integer[], IN red_2 integer[], IN green_2 integer[], IN blue_2 integer[])
    RETURNS integer
    LANGUAGE 'plpgsql'
    STABLE STRICT PARALLEL SAFE 
AS $BODY$
DECLARE
    d integer;
BEGIN
    d := 0;
    FOR i IN 1..4 LOOP
        d := d + ABS(red_1[i] - red_2[i]);
        d := d + ABS(green_1[i] - green_2[i]);
        d := d + ABS(blue_1[i] - blue_2[i]);
    END LOOP;
    RETURN d;
END;
$BODY$;

ALTER FUNCTION public.abs_norm(integer[], integer[], integer[], integer[], integer[], integer[])
    OWNER TO postgres;
"""


EUCL_NORM_FUNC = """
CREATE OR REPLACE FUNCTION public.eucl_norm(IN red_1 integer[], IN green_1 integer[], IN blue_1 integer[], IN red_2 integer[], IN green_2 integer[], IN blue_2 integer[])
    RETURNS numeric
    LANGUAGE 'plpgsql'
    STABLE STRICT PARALLEL SAFE 
AS $BODY$
DECLARE
    d bigint;
BEGIN
    d := 0;
    FOR i IN 1..4 LOOP
        d := d + (red_1[i] - red_2[i]) ^ 2;
        d := d + (green_1[i] - green_2[i]) ^ 2;
        d := d + (blue_1[i] - blue_2[i]) ^ 2;
    END LOOP;
    RETURN |/ d;
END;
$BODY$;

ALTER FUNCTION public.eucl_norm(integer[], integer[], integer[], integer[], integer[], integer[])
    OWNER TO postgres;
"""


DHASH_XOR_FUNC = """
CREATE OR REPLACE FUNCTION public.dhash_xor_norm(IN red_1 bit, IN green_1 bit, IN blue_1 bit, IN red_2 bit, IN green_2 bit, IN blue_2 bit)
    RETURNS integer
    LANGUAGE 'plpgsql'
    STABLE STRICT PARALLEL SAFE 
AS $BODY$
DECLARE
    b integer;
BEGIN
    b := bit_count(red_1 # red_2) + bit_count(green_1 # green_2) + bit_count(blue_1 # blue_2);
    RETURN b;
END;
$BODY$;

ALTER FUNCTION public.dhash_xor_norm(bit, bit, bit, bit, bit, bit)
    OWNER TO postgres;
"""


SIMILARITY_FUNC = """
SELECT public.image.url, public.submission.id, {alg}(
    red, green, blue, {red}, {green}, {blue}
    ) as similarity
FROM 
	public.{model} 
LEFT JOIN public.image
	ON public.{model}.id = public.image.id
LEFT JOIN public.submission
	ON public.image.submission_id = public.submission.id
ORDER BY similarity ASC
LIMIT {quantity}
"""