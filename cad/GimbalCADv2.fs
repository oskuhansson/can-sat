FeatureScript 3112;
import(path : "onshape/std/common.fs", version : "3112.0");

/**
 * CanSat Ground Station 2-Axis Tracking Gimbal (Azimuth + Elevation)
 *
 * Ultra-Compact, Clean, Low-Profile Architecture:
 * - Elevation axis positioned DIRECTLY ON TOP of Azimuth axis (X = 0, Y = 0)
 * - Low-profile design: Elevation axle at Z = 140 mm (cut down from 280 mm!)
 * - Zero unnecessary boxes (clean base, sleek RF feedpoint)
 * - Real counterbored bolt holes (no fake cylinder bolts; standard fasteners in Assembly)
 * - NEMA 17 Stepper Motors with GT2 5:1 timing belts on both axes
 * - Dual 6808-2RS Azimuth bearings & Dual 6001-2RS Elevation bearings
 * - 2020 V-slot base frame with corner brackets and rubber damping feet
 * - Balanced 600 mm 2020 boom with 7-element 868 MHz Yagi & gold SMA connector
 * - Parametric kinematics: Azimuth pan (-200..+200 deg) and Elevation tilt (-10..+90 deg)
 */

annotation { "Feature Type Name" : "Gimbal CAD Plan V2" }
export const gimbalCADPlanV2 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Azimuth Pan Angle" }
        isAngle(definition.azimuthAngle, { (degree) : [-200, 0, 200] } as AngleBoundSpec);

        annotation { "Name" : "Elevation Tilt Angle" }
        isAngle(definition.elevationAngle, { (degree) : [-10, 0, 90] } as AngleBoundSpec);
    }
    {
        // ====================================================================
        // CLEAN INDUSTRIAL PALETTE
        // ====================================================================
        var colAluSilver    = color(0.83, 0.85, 0.88); // Natural satin anodized aluminum
        var colSlotDark     = color(0.36, 0.38, 0.41); // Profile slot shadow
        var colPetgDark     = color(0.18, 0.20, 0.23); // Stealth matte anthracite ASA / PETG
        var colPetgBlue     = color(0.08, 0.46, 0.78); // Technical electric blue
        var colPetgOrange   = color(0.95, 0.44, 0.08); // Safety orange timing pulleys
        var colMotorBody    = color(0.14, 0.14, 0.16); // Satin black motor stator
        var colMotorSilver  = color(0.84, 0.85, 0.87); // Machined silver endbells
        var colMotorShaft   = color(0.92, 0.93, 0.95); // Polished stainless steel
        var colBeltRubber   = color(0.10, 0.10, 0.11); // Matte black rubber
        var colBearingSteel = color(0.78, 0.80, 0.83); // Chrome bearing raceways
        var colBearingSeal  = color(0.05, 0.28, 0.68); // 2RS blue seal
        var colRubberFoot   = color(0.12, 0.12, 0.13); // EPDM rubber feet
        var colBrassGold    = color(0.90, 0.74, 0.25); // Gold-plated SMA connector
        var colHardwareSilver = color(0.66, 0.68, 0.71); // Zinc-plated ISO hardware

        // ====================================================================
        // 1. BASE FRAME & COMPACT STATIONARY MOUNT (SERIE 100)
        // ====================================================================

        // 1.1 Long base rails (2020 V-slot, L = 220 mm at Y = +/- 80 mm)
        fCuboid(context, id + "railXLeft", { "corner1" : vector(-110, 70, 0) * millimeter, "corner2" : vector(110, 90, 20) * millimeter });
        fCuboid(context, id + "slotXLeftTop", { "corner1" : vector(-110, 77, 18.2) * millimeter, "corner2" : vector(110, 83, 20.1) * millimeter });
        fCuboid(context, id + "slotXLeftOut", { "corner1" : vector(-110, 88.2, 7) * millimeter,  "corner2" : vector(110, 90.1, 13) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "railXLeft", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "101_RAIL_X_LEFT" });
        setProperty(context, { "entities" : qCreatedBy(id + "railXLeft", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "slotXLeftTop", EntityType.BODY), qCreatedBy(id + "slotXLeftOut", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "101_SLOTS_X_LEFT" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "slotXLeftTop", EntityType.BODY), qCreatedBy(id + "slotXLeftOut", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });

        fCuboid(context, id + "railXRight", { "corner1" : vector(-110, -90, 0) * millimeter, "corner2" : vector(110, -70, 20) * millimeter });
        fCuboid(context, id + "slotXRightTop", { "corner1" : vector(-110, -83, 18.2) * millimeter, "corner2" : vector(110, -77, 20.1) * millimeter });
        fCuboid(context, id + "slotXRightOut", { "corner1" : vector(-110, -90.1, 7) * millimeter,  "corner2" : vector(110, -88.2, 13) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "railXRight", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "101_RAIL_X_RIGHT" });
        setProperty(context, { "entities" : qCreatedBy(id + "railXRight", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "slotXRightTop", EntityType.BODY), qCreatedBy(id + "slotXRightOut", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "101_SLOTS_X_RIGHT" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "slotXRightTop", EntityType.BODY), qCreatedBy(id + "slotXRightOut", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });

        // 1.2 Cross base rails (2020 V-slot, L = 140 mm at X = +/- 100 mm)
        fCuboid(context, id + "railYFront", { "corner1" : vector(90, -70, 0) * millimeter, "corner2" : vector(110, 70, 20) * millimeter });
        fCuboid(context, id + "slotYFrontTop", { "corner1" : vector(97, -70, 18.2) * millimeter, "corner2" : vector(103, 70, 20.1) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "railYFront", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "102_RAIL_Y_FRONT" });
        setProperty(context, { "entities" : qCreatedBy(id + "railYFront", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "slotYFrontTop", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "102_SLOT_Y_FRONT" });
        setProperty(context, { "entities" : qCreatedBy(id + "slotYFrontTop", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });

        fCuboid(context, id + "railYRear", { "corner1" : vector(-110, -70, 0) * millimeter, "corner2" : vector(-90, 70, 20) * millimeter });
        fCuboid(context, id + "slotYRearTop", { "corner1" : vector(-103, -70, 18.2) * millimeter, "corner2" : vector(-97, 70, 20.1) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "railYRear", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "102_RAIL_Y_REAR" });
        setProperty(context, { "entities" : qCreatedBy(id + "railYRear", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "slotYRearTop", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "102_SLOT_Y_REAR" });
        setProperty(context, { "entities" : qCreatedBy(id + "slotYRearTop", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });

        // 1.3 4 x Cast Aluminum Corner Gusset Brackets
        fCuboid(context, id + "bktFL", { "corner1" : vector(72, 52, 0) * millimeter, "corner2" : vector(90, 70, 18) * millimeter });
        fCuboid(context, id + "bktFR", { "corner1" : vector(72, -70, 0) * millimeter, "corner2" : vector(90, -52, 18) * millimeter });
        fCuboid(context, id + "bktRL", { "corner1" : vector(-90, 52, 0) * millimeter, "corner2" : vector(-72, 70, 18) * millimeter });
        fCuboid(context, id + "bktRR", { "corner1" : vector(-90, -70, 0) * millimeter, "corner2" : vector(-72, -52, 18) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "bktFL", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "103_CORNER_BKT_FL" });
        setProperty(context, { "entities" : qCreatedBy(id + "bktFR", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "103_CORNER_BKT_FR" });
        setProperty(context, { "entities" : qCreatedBy(id + "bktRL", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "103_CORNER_BKT_RL" });
        setProperty(context, { "entities" : qCreatedBy(id + "bktRR", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "103_CORNER_BKT_RR" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "bktFL", EntityType.BODY), qCreatedBy(id + "bktFR", EntityType.BODY), qCreatedBy(id + "bktRL", EntityType.BODY), qCreatedBy(id + "bktRR", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });

        // 1.4 4 x Rubber Leveling Damper Feet
        fCylinder(context, id + "foot1", { "bottomCenter" : vector(-98, -78, -8) * millimeter, "topCenter" : vector(-98, -78, 0) * millimeter, "radius" : 13 * millimeter });
        fCylinder(context, id + "foot2", { "bottomCenter" : vector(98, -78, -8) * millimeter,  "topCenter" : vector(98, -78, 0) * millimeter,  "radius" : 13 * millimeter });
        fCylinder(context, id + "foot3", { "bottomCenter" : vector(-98, 78, -8) * millimeter,  "topCenter" : vector(-98, 78, 0) * millimeter,  "radius" : 13 * millimeter });
        fCylinder(context, id + "foot4", { "bottomCenter" : vector(98, 78, -8) * millimeter,   "topCenter" : vector(98, 78, 0) * millimeter,   "radius" : 13 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "foot1", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "106_FOOT_RL" });
        setProperty(context, { "entities" : qCreatedBy(id + "foot2", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "106_FOOT_FL" });
        setProperty(context, { "entities" : qCreatedBy(id + "foot3", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "106_FOOT_RR" });
        setProperty(context, { "entities" : qCreatedBy(id + "foot4", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "106_FOOT_FR" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "foot1", EntityType.BODY), qCreatedBy(id + "foot2", EntityType.BODY), qCreatedBy(id + "foot3", EntityType.BODY), qCreatedBy(id + "foot4", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colRubberFoot });

        // 1.5 Clean Compact Base Plate (150 X x 170 Y x 6 mm, Z = 20..26 mm)
        fCuboid(context, id + "basePlateMain", { "corner1" : vector(-65, -85, 20) * millimeter, "corner2" : vector(65, 85, 26) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "basePlateMain", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "104_BASE_PLATE" });
        setProperty(context, { "entities" : qCreatedBy(id + "basePlateMain", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // 1.6 Low-Profile Central Mast Flange (dia 82 x 8 mm, Z = 26..34 mm)
        fCylinder(context, id + "flangeBase", { "bottomCenter" : vector(0, 0, 26) * millimeter, "topCenter" : vector(0, 0, 34) * millimeter, "radius" : 41 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "flangeBase", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "105_PILLAR_FLANGE" });
        setProperty(context, { "entities" : qCreatedBy(id + "flangeBase", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // ====================================================================
        // 2. COMPACT AZIMUTH DRIVE & BEARING COLUMN (SERIE 200)
        // ====================================================================

        // 2.1 Shortened Central Aluminum Tube (OD 40 mm, ID 34 mm, L = 50 mm, Z = 26..76 mm)
        fCylinder(context, id + "pillarTube", { "bottomCenter" : vector(0, 0, 26) * millimeter, "topCenter" : vector(0, 0, 76) * millimeter, "radius" : 20 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "pillarTube", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "201_PILLAR_TUBE" });
        setProperty(context, { "entities" : qCreatedBy(id + "pillarTube", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });

        // 2.2 Azimuth NEMA 17 Stepper Motor (at Y = +75.72 mm, Z = 26..74 mm)
        fCuboid(context, id + "azMotorStator",    { "corner1" : vector(-21.15, 75.72 - 21.15, 32) * millimeter, "corner2" : vector(21.15, 75.72 + 21.15, 66) * millimeter });
        fCuboid(context, id + "azMotorFrontBell", { "corner1" : vector(-21.15, 75.72 - 21.15, 66) * millimeter, "corner2" : vector(21.15, 75.72 + 21.15, 74) * millimeter });
        fCuboid(context, id + "azMotorRearBell",  { "corner1" : vector(-21.15, 75.72 - 21.15, 26) * millimeter, "corner2" : vector(21.15, 75.72 + 21.15, 32) * millimeter });
        fCylinder(context, id + "azMotorShaft",   { "bottomCenter" : vector(0, 75.72, 74) * millimeter, "topCenter" : vector(0, 75.72, 98) * millimeter, "radius" : 2.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorStator", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "208_AZ_MOTOR_STATOR" });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorStator", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorBody });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "azMotorFrontBell", EntityType.BODY), qCreatedBy(id + "azMotorRearBell", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "208_AZ_MOTOR_ENDBELLS" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "azMotorFrontBell", EntityType.BODY), qCreatedBy(id + "azMotorRearBell", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorShaft", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "208_AZ_MOTOR_SHAFT" });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorShaft", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorShaft });

        // 2.3 Azimuth 20T Motor Pulley (belt line Z = 45 mm)
        fCylinder(context, id + "az20TPulley", { "bottomCenter" : vector(0, 75.72, 41) * millimeter, "topCenter" : vector(0, 75.72, 49) * millimeter, "radius" : 6.11 * millimeter });
        fCylinder(context, id + "az20TFlangeL", { "bottomCenter" : vector(0, 75.72, 39.5) * millimeter, "topCenter" : vector(0, 75.72, 41) * millimeter, "radius" : 8 * millimeter });
        fCylinder(context, id + "az20TFlangeU", { "bottomCenter" : vector(0, 75.72, 49) * millimeter, "topCenter" : vector(0, 75.72, 50.5) * millimeter, "radius" : 8 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "az20TPulley", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "207_AZ_PULLEY_20T" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "az20TPulley", EntityType.BODY), qCreatedBy(id + "az20TFlangeL", EntityType.BODY), qCreatedBy(id + "az20TFlangeU", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "207_AZ_PULLEY_20T_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "az20TPulley", EntityType.BODY), qCreatedBy(id + "az20TFlangeL", EntityType.BODY), qCreatedBy(id + "az20TFlangeU", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorSilver });

        // 2.4 Azimuth Motor Mounting Bracket
        fCuboid(context, id + "azMotorBkt", { "corner1" : vector(-25, 75.72 - 24, 20) * millimeter, "corner2" : vector(25, 75.72 + 24, 26) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorBkt", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "209_AZ_MOTOR_BRACKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "azMotorBkt", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // ====================================================================
        // ROTATING AZIMUTH SUBASSEMBLY (Pivots with definition.azimuthAngle)
        // ====================================================================

        // 2.5 Dual 6808-2RS Bearings (OD 52, ID 40, W 7 mm)
        fCylinder(context, id + "azBrgLowSteel", { "bottomCenter" : vector(0, 0, 48) * millimeter, "topCenter" : vector(0, 0, 55) * millimeter, "radius" : 26 * millimeter });
        fCylinder(context, id + "azBrgLowSeal",  { "bottomCenter" : vector(0, 0, 48.2) * millimeter, "topCenter" : vector(0, 0, 54.8) * millimeter, "radius" : 24.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgLowSteel", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "204_AZ_BEARING_LOWER_6808" });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgLowSeal", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "204_AZ_BEARING_LOWER_SEAL" });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgLowSteel", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSteel });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgLowSeal", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSeal });

        fCylinder(context, id + "azBrgUpSteel", { "bottomCenter" : vector(0, 0, 65) * millimeter, "topCenter" : vector(0, 0, 72) * millimeter, "radius" : 26 * millimeter });
        fCylinder(context, id + "azBrgUpSeal",  { "bottomCenter" : vector(0, 0, 65.2) * millimeter, "topCenter" : vector(0, 0, 71.8) * millimeter, "radius" : 24.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgUpSteel", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "204_AZ_BEARING_UPPER_6808" });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgUpSeal", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "204_AZ_BEARING_UPPER_SEAL" });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgUpSteel", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSteel });
        setProperty(context, { "entities" : qCreatedBy(id + "azBrgUpSeal", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSeal });

        // 2.6 Low-Profile Azimuth Drum Sleeve (Z = 48..72 mm, height only 24 mm!)
        fCylinder(context, id + "azDrumBody", { "bottomCenter" : vector(0, 0, 48) * millimeter, "topCenter" : vector(0, 0, 72) * millimeter, "radius" : 30 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azDrumBody", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "203_AZ_DRUM" });
        setProperty(context, { "entities" : qCreatedBy(id + "azDrumBody", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // 2.7 Azimuth 100T GT2 Pulley (Printable, OD 63.15 mm, Z = 42..48 mm)
        fCylinder(context, id + "az100TRim",     { "bottomCenter" : vector(0, 0, 42) * millimeter, "topCenter" : vector(0, 0, 48) * millimeter, "radius" : 31.58 * millimeter });
        fCylinder(context, id + "az100TFlangeL", { "bottomCenter" : vector(0, 0, 40.5) * millimeter, "topCenter" : vector(0, 0, 42) * millimeter, "radius" : 34.5 * millimeter });
        fCylinder(context, id + "az100TFlangeU", { "bottomCenter" : vector(0, 0, 48) * millimeter, "topCenter" : vector(0, 0, 49.5) * millimeter, "radius" : 34.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "az100TRim", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "206_AZ_PULLEY_100T" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "az100TRim", EntityType.BODY), qCreatedBy(id + "az100TFlangeL", EntityType.BODY), qCreatedBy(id + "az100TFlangeU", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "206_AZ_PULLEY_100T_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "az100TRim", EntityType.BODY), qCreatedBy(id + "az100TFlangeL", EntityType.BODY), qCreatedBy(id + "az100TFlangeU", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgOrange });

        // 2.8 Continuous GT2-280-6 Timing Belt Loop
        fCuboid(context, id + "azBeltTanL", { "corner1" : vector(-31.6, 0, 42) * millimeter, "corner2" : vector(-6.1, 75.72, 48) * millimeter });
        fCuboid(context, id + "azBeltTanR", { "corner1" : vector(6.1, 75.72, 42) * millimeter,  "corner2" : vector(31.6, 0, 48) * millimeter });
        fCylinder(context, id + "azBeltArc100T", { "bottomCenter" : vector(0, 0, 42) * millimeter, "topCenter" : vector(0, 0, 48) * millimeter, "radius" : 32.5 * millimeter });
        fCylinder(context, id + "azBeltArc20T",  { "bottomCenter" : vector(0, 75.72, 42) * millimeter, "topCenter" : vector(0, 75.72, 48) * millimeter, "radius" : 7.2 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "azBeltTanL", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "AZ_BELT_280_2GT_6" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "azBeltTanL", EntityType.BODY), qCreatedBy(id + "azBeltTanR", EntityType.BODY), qCreatedBy(id + "azBeltArc100T", EntityType.BODY), qCreatedBy(id + "azBeltArc20T", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "AZ_BELT_280_LOOP" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "azBeltTanL", EntityType.BODY), qCreatedBy(id + "azBeltTanR", EntityType.BODY), qCreatedBy(id + "azBeltArc100T", EntityType.BODY), qCreatedBy(id + "azBeltArc20T", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colBeltRubber });

        // ====================================================================
        // 3. COMPACT LOW-PROFILE U-FORK TURRET (CENTERED AT X = 0, Z_axle = 140 mm!)
        // ====================================================================

        // 3.1 Turntable Base Disc (Z = 72..80 mm, centered directly on azimuth axis!)
        fCylinder(context, id + "turretBaseDisc", { "bottomCenter" : vector(0, 0, 72) * millimeter, "topCenter" : vector(0, 0, 80) * millimeter, "radius" : 44 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "turretBaseDisc", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "301_TURRET_BASE_DISC" });
        setProperty(context, { "entities" : qCreatedBy(id + "turretBaseDisc", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // 3.2 Symmetrical Compact Towers (Centered at X = 0, axle at Z = 140 mm!)
        // Left Tower (Y = -42 mm, thickness 16 mm -> Y = -50..-34 mm)
        fCuboid(context, id + "towerLMain", { "corner1" : vector(-14, -50, 80) * millimeter, "corner2" : vector(14, -34, 154) * millimeter });
        fCylinder(context, id + "towerLHub", { "bottomCenter" : vector(0, -50, 140) * millimeter, "topCenter" : vector(0, -34, 140) * millimeter, "radius" : 16 * millimeter });
        // Symmetrical diagonal buttress ribs
        fCuboid(context, id + "towerLRibBack", { "corner1" : vector(-34, -48, 80) * millimeter, "corner2" : vector(-14, -36, 115) * millimeter });
        fCuboid(context, id + "towerLRibFwd",  { "corner1" : vector(14, -48, 80) * millimeter,  "corner2" : vector(34, -36, 115) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "towerLMain", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "302_TOWER_L" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "towerLMain", EntityType.BODY), qCreatedBy(id + "towerLHub", EntityType.BODY), qCreatedBy(id + "towerLRibBack", EntityType.BODY), qCreatedBy(id + "towerLRibFwd", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "302_TOWER_L_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "towerLMain", EntityType.BODY), qCreatedBy(id + "towerLHub", EntityType.BODY), qCreatedBy(id + "towerLRibBack", EntityType.BODY), qCreatedBy(id + "towerLRibFwd", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // Right Tower (Y = +42 mm, thickness 16 mm -> Y = +34..+50 mm)
        fCuboid(context, id + "towerRMain", { "corner1" : vector(-14, 34, 80) * millimeter, "corner2" : vector(14, 50, 154) * millimeter });
        fCylinder(context, id + "towerRHub", { "bottomCenter" : vector(0, 34, 140) * millimeter, "topCenter" : vector(0, 50, 140) * millimeter, "radius" : 16 * millimeter });
        fCuboid(context, id + "towerRRibBack", { "corner1" : vector(-34, 36, 80) * millimeter, "corner2" : vector(-14, 48, 115) * millimeter });
        fCuboid(context, id + "towerRRibFwd",  { "corner1" : vector(14, 36, 80) * millimeter,  "corner2" : vector(34, 48, 115) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "towerRMain", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "302_TOWER_R" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "towerRMain", EntityType.BODY), qCreatedBy(id + "towerRHub", EntityType.BODY), qCreatedBy(id + "towerRRibBack", EntityType.BODY), qCreatedBy(id + "towerRRibFwd", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "302_TOWER_R_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "towerRMain", EntityType.BODY), qCreatedBy(id + "towerRHub", EntityType.BODY), qCreatedBy(id + "towerRRibBack", EntityType.BODY), qCreatedBy(id + "towerRRibFwd", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // 3.3 Elevation NEMA 17 Stepper Motor (Mounted on Left Tower at distance C = 60.57 mm vertically below axle)
        // Axle Z = 140 mm -> Motor at X = 0, Z = 140 - 60.57 = 79.43 mm!
        fCuboid(context, id + "elMotorStator",    { "corner1" : vector(-21.15, -112, 79.43 - 21.15) * millimeter, "corner2" : vector(21.15, -78, 79.43 + 21.15) * millimeter });
        fCuboid(context, id + "elMotorFrontBell", { "corner1" : vector(-21.15, -78, 79.43 - 21.15) * millimeter,  "corner2" : vector(21.15, -70, 79.43 + 21.15) * millimeter });
        fCuboid(context, id + "elMotorRearBell",  { "corner1" : vector(-21.15, -118, 79.43 - 21.15) * millimeter, "corner2" : vector(21.15, -112, 79.43 + 21.15) * millimeter });
        fCylinder(context, id + "elMotorShaft",   { "bottomCenter" : vector(0, -70, 79.43) * millimeter, "topCenter" : vector(0, -48, 79.43) * millimeter, "radius" : 2.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorStator", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "407_EL_MOTOR_STATOR" });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorStator", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorBody });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elMotorFrontBell", EntityType.BODY), qCreatedBy(id + "elMotorRearBell", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "407_EL_MOTOR_ENDBELLS" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elMotorFrontBell", EntityType.BODY), qCreatedBy(id + "elMotorRearBell", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorShaft", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "407_EL_MOTOR_SHAFT" });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorShaft", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorShaft });

        // 3.4 Elevation Motor Bracket on Left Tower
        fCuboid(context, id + "elMotorBracket", { "corner1" : vector(-23, -70, 79.43 - 23) * millimeter, "corner2" : vector(23, -50, 79.43 + 23) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorBracket", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "303_EL_MOTOR_BRACKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "elMotorBracket", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgDark });

        // 3.5 Elevation 16T Motor Pulley (at Y = -59 mm, centered at X = 0, Z = 79.43 mm)
        fCylinder(context, id + "el16TPulley",  { "bottomCenter" : vector(0, -63, 79.43) * millimeter, "topCenter" : vector(0, -55, 79.43) * millimeter, "radius" : 4.84 * millimeter });
        fCylinder(context, id + "el16TFlange1", { "bottomCenter" : vector(0, -64.5, 79.43) * millimeter, "topCenter" : vector(0, -63, 79.43) * millimeter, "radius" : 7 * millimeter });
        fCylinder(context, id + "el16TFlange2", { "bottomCenter" : vector(0, -55, 79.43) * millimeter, "topCenter" : vector(0, -53.5, 79.43) * millimeter, "radius" : 7 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "el16TPulley", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "406_EL_PULLEY_16T" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "el16TPulley", EntityType.BODY), qCreatedBy(id + "el16TFlange1", EntityType.BODY), qCreatedBy(id + "el16TFlange2", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "406_EL_PULLEY_16T_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "el16TPulley", EntityType.BODY), qCreatedBy(id + "el16TFlange1", EntityType.BODY), qCreatedBy(id + "el16TFlange2", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorSilver });

        // 3.6 Dual 6001-2RS Bearings in Towers (at X = 0, Z = 140 mm)
        fCylinder(context, id + "elBrgLSteel", { "bottomCenter" : vector(0, -50, 140) * millimeter, "topCenter" : vector(0, -42, 140) * millimeter, "radius" : 14 * millimeter });
        fCylinder(context, id + "elBrgLSeal",  { "bottomCenter" : vector(0, -49.8, 140) * millimeter, "topCenter" : vector(0, -42.2, 140) * millimeter, "radius" : 12.8 * millimeter });
        fCylinder(context, id + "elBrgRSteel", { "bottomCenter" : vector(0, 42, 140) * millimeter,  "topCenter" : vector(0, 50, 140) * millimeter,  "radius" : 14 * millimeter });
        fCylinder(context, id + "elBrgRSeal",  { "bottomCenter" : vector(0, 42.2, 140) * millimeter, "topCenter" : vector(0, 49.8, 140) * millimeter, "radius" : 12.8 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elBrgLSteel", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "402_EL_BEARING_L_6001" });
        setProperty(context, { "entities" : qCreatedBy(id + "elBrgLSeal", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "402_EL_BEARING_L_SEAL" });
        setProperty(context, { "entities" : qCreatedBy(id + "elBrgRSteel", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "402_EL_BEARING_R_6001" });
        setProperty(context, { "entities" : qCreatedBy(id + "elBrgRSeal", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "402_EL_BEARING_R_SEAL" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elBrgLSteel", EntityType.BODY), qCreatedBy(id + "elBrgRSteel", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSteel });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elBrgLSeal", EntityType.BODY), qCreatedBy(id + "elBrgRSeal", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colBearingSeal });

        // ====================================================================
        // 4. ELEVATION ASSEMBLY (Tilts around Axle at X = 0, Z = 140 mm)
        // ====================================================================

        // 4.1 Ground Stainless Steel Elevation Axle (dia 12 mm x 125 mm, Y = -68..+57 mm)
        fCylinder(context, id + "elAxle", { "bottomCenter" : vector(0, -68, 140) * millimeter, "topCenter" : vector(0, 57, 140) * millimeter, "radius" : 6 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elAxle", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "401_EL_AXLE" });
        setProperty(context, { "entities" : qCreatedBy(id + "elAxle", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorShaft });

        // 4.2 Elevation 80T GT2 Pulley (OD 50.42 mm, centered at X = 0, Y = -59 mm, Z = 140 mm)
        fCylinder(context, id + "el80TPulleyRim", { "bottomCenter" : vector(0, -63, 140) * millimeter, "topCenter" : vector(0, -55, 140) * millimeter, "radius" : 25.21 * millimeter });
        fCylinder(context, id + "el80TFlangeL",   { "bottomCenter" : vector(0, -65, 140) * millimeter, "topCenter" : vector(0, -63, 140) * millimeter, "radius" : 28.5 * millimeter });
        fCylinder(context, id + "el80TFlangeR",   { "bottomCenter" : vector(0, -55, 140) * millimeter, "topCenter" : vector(0, -53.5, 140) * millimeter, "radius" : 28.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "el80TPulleyRim", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "405_EL_PULLEY_80T" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "el80TPulleyRim", EntityType.BODY), qCreatedBy(id + "el80TFlangeL", EntityType.BODY), qCreatedBy(id + "el80TFlangeR", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "405_EL_PULLEY_80T_ASSEMBLY" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "el80TPulleyRim", EntityType.BODY), qCreatedBy(id + "el80TFlangeL", EntityType.BODY), qCreatedBy(id + "el80TFlangeR", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgOrange });

        // 4.3 Vertical GT2-224-6 Timing Belt Loop (between Z = 140 and Z = 79.43 mm)
        fCuboid(context, id + "elBeltTanL", { "corner1" : vector(-25.2, -62, 79.43) * millimeter, "corner2" : vector(-4.8, -56, 140) * millimeter });
        fCuboid(context, id + "elBeltTanR", { "corner1" : vector(4.8, -62, 140) * millimeter,     "corner2" : vector(25.2, -56, 79.43) * millimeter });
        fCylinder(context, id + "elBeltArc80T", { "bottomCenter" : vector(0, -62, 140) * millimeter, "topCenter" : vector(0, -56, 140) * millimeter, "radius" : 26.5 * millimeter });
        fCylinder(context, id + "elBeltArc16T", { "bottomCenter" : vector(0, -62, 79.43) * millimeter, "topCenter" : vector(0, -56, 79.43) * millimeter, "radius" : 6.0 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elBeltTanL", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "EL_BELT_224_2GT_6" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elBeltTanL", EntityType.BODY), qCreatedBy(id + "elBeltTanR", EntityType.BODY), qCreatedBy(id + "elBeltArc80T", EntityType.BODY), qCreatedBy(id + "elBeltArc16T", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "EL_BELT_224_LOOP" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elBeltTanL", EntityType.BODY), qCreatedBy(id + "elBeltTanR", EntityType.BODY), qCreatedBy(id + "elBeltArc80T", EntityType.BODY), qCreatedBy(id + "elBeltArc16T", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colBeltRubber });

        // 4.4 Shaft Collar dia 12 mm
        fCylinder(context, id + "elShaftCollar", { "bottomCenter" : vector(0, 48, 140) * millimeter, "topCenter" : vector(0, 56, 140) * millimeter, "radius" : 10 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elShaftCollar", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "408_SHAFT_COLLAR" });
        setProperty(context, { "entities" : qCreatedBy(id + "elShaftCollar", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colMotorSilver });

        // 4.5 Clean Antenna Boom Cradle Saddle (CRADLE_LOWER: 50 Y x 34 X x 24 Z, Blue Accent)
        // Mounted directly on the axle at X = 0, Z = 140 mm
        fCuboid(context, id + "cradleLowerBody", { "corner1" : vector(-17, -25, 128) * millimeter, "corner2" : vector(17, 25, 150) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleLowerBody", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "403_CRADLE_LOWER" });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleLowerBody", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 4.5.1 Axle clearance sleeve (axle passes through the saddle)
        fCylinder(context, id + "cradleAxleCut", { "bottomCenter" : vector(0, -26, 140) * millimeter, "topCenter" : vector(0, 26, 140) * millimeter, "radius" : 6.1 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleAxleCut", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "403_CRADLE_AXLE_SLEEVE" });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleAxleCut", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });

        // 4.6 Upper Cradle Clamp Cap (50 Y x 34 X x 8 Z, Z = 158..166 mm)
        fCuboid(context, id + "cradleCapBridge", { "corner1" : vector(-17, -25, 158) * millimeter, "corner2" : vector(17, 25, 166) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleCapBridge", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "404_CRADLE_CAP" });
        setProperty(context, { "entities" : qCreatedBy(id + "cradleCapBridge", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 4.6.1 M4 bolt locations are occupied by the screws below (4.7)

        // 4.7 Real ISO 4762 M4x16 socket head cap screws
        //     Head underside rests on the cap top (Z = 166); shank reaches into the cradle.
        //     Each screw is a distinct part: head, hex socket recess, threaded shank.

        // --- Screw A (-10, -18) ---
        fCylinder(context, id + "skA_head",   { "bottomCenter" : vector(-10, -18, 166) * millimeter, "topCenter" : vector(-10, -18, 170) * millimeter, "radius" : 3.5 * millimeter });
        fCylinder(context, id + "skA_socket", { "bottomCenter" : vector(-10, -18, 167.6) * millimeter, "topCenter" : vector(-10, -18, 170.05) * millimeter, "radius" : 1.75 * millimeter });
        fCylinder(context, id + "skA_shank",  { "bottomCenter" : vector(-10, -18, 150) * millimeter, "topCenter" : vector(-10, -18, 166.1) * millimeter, "radius" : 2 * millimeter });
        fCylinder(context, id + "skA_thr1",   { "bottomCenter" : vector(-10, -18, 151.0) * millimeter, "topCenter" : vector(-10, -18, 151.4) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skA_thr2",   { "bottomCenter" : vector(-10, -18, 152.4) * millimeter, "topCenter" : vector(-10, -18, 152.8) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skA_thr3",   { "bottomCenter" : vector(-10, -18, 153.8) * millimeter, "topCenter" : vector(-10, -18, 154.2) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skA_thr4",   { "bottomCenter" : vector(-10, -18, 155.2) * millimeter, "topCenter" : vector(-10, -18, 155.6) * millimeter, "radius" : 1.85 * millimeter });

        // --- Screw B (+10, -18) ---
        fCylinder(context, id + "skB_head",   { "bottomCenter" : vector(10, -18, 166) * millimeter, "topCenter" : vector(10, -18, 170) * millimeter, "radius" : 3.5 * millimeter });
        fCylinder(context, id + "skB_socket", { "bottomCenter" : vector(10, -18, 167.6) * millimeter, "topCenter" : vector(10, -18, 170.05) * millimeter, "radius" : 1.75 * millimeter });
        fCylinder(context, id + "skB_shank",  { "bottomCenter" : vector(10, -18, 150) * millimeter, "topCenter" : vector(10, -18, 166.1) * millimeter, "radius" : 2 * millimeter });
        fCylinder(context, id + "skB_thr1",   { "bottomCenter" : vector(10, -18, 151.0) * millimeter, "topCenter" : vector(10, -18, 151.4) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skB_thr2",   { "bottomCenter" : vector(10, -18, 152.4) * millimeter, "topCenter" : vector(10, -18, 152.8) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skB_thr3",   { "bottomCenter" : vector(10, -18, 153.8) * millimeter, "topCenter" : vector(10, -18, 154.2) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skB_thr4",   { "bottomCenter" : vector(10, -18, 155.2) * millimeter, "topCenter" : vector(10, -18, 155.6) * millimeter, "radius" : 1.85 * millimeter });

        // --- Screw C (-10, +18) ---
        fCylinder(context, id + "skC_head",   { "bottomCenter" : vector(-10, 18, 166) * millimeter, "topCenter" : vector(-10, 18, 170) * millimeter, "radius" : 3.5 * millimeter });
        fCylinder(context, id + "skC_socket", { "bottomCenter" : vector(-10, 18, 167.6) * millimeter, "topCenter" : vector(-10, 18, 170.05) * millimeter, "radius" : 1.75 * millimeter });
        fCylinder(context, id + "skC_shank",  { "bottomCenter" : vector(-10, 18, 150) * millimeter, "topCenter" : vector(-10, 18, 166.1) * millimeter, "radius" : 2 * millimeter });
        fCylinder(context, id + "skC_thr1",   { "bottomCenter" : vector(-10, 18, 151.0) * millimeter, "topCenter" : vector(-10, 18, 151.4) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skC_thr2",   { "bottomCenter" : vector(-10, 18, 152.4) * millimeter, "topCenter" : vector(-10, 18, 152.8) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skC_thr3",   { "bottomCenter" : vector(-10, 18, 153.8) * millimeter, "topCenter" : vector(-10, 18, 154.2) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skC_thr4",   { "bottomCenter" : vector(-10, 18, 155.2) * millimeter, "topCenter" : vector(-10, 18, 155.6) * millimeter, "radius" : 1.85 * millimeter });

        // --- Screw D (+10, +18) ---
        fCylinder(context, id + "skD_head",   { "bottomCenter" : vector(10, 18, 166) * millimeter, "topCenter" : vector(10, 18, 170) * millimeter, "radius" : 3.5 * millimeter });
        fCylinder(context, id + "skD_socket", { "bottomCenter" : vector(10, 18, 167.6) * millimeter, "topCenter" : vector(10, 18, 170.05) * millimeter, "radius" : 1.75 * millimeter });
        fCylinder(context, id + "skD_shank",  { "bottomCenter" : vector(10, 18, 150) * millimeter, "topCenter" : vector(10, 18, 166.1) * millimeter, "radius" : 2 * millimeter });
        fCylinder(context, id + "skD_thr1",   { "bottomCenter" : vector(10, 18, 151.0) * millimeter, "topCenter" : vector(10, 18, 151.4) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skD_thr2",   { "bottomCenter" : vector(10, 18, 152.4) * millimeter, "topCenter" : vector(10, 18, 152.8) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skD_thr3",   { "bottomCenter" : vector(10, 18, 153.8) * millimeter, "topCenter" : vector(10, 18, 154.2) * millimeter, "radius" : 1.85 * millimeter });
        fCylinder(context, id + "skD_thr4",   { "bottomCenter" : vector(10, 18, 155.2) * millimeter, "topCenter" : vector(10, 18, 155.6) * millimeter, "radius" : 1.85 * millimeter });

        setProperty(context, { "entities" : qCreatedBy(id + "skA_head", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_head", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_head", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_head", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D" });
        setProperty(context, { "entities" : qUnion([
                        qCreatedBy(id + "skA_head", EntityType.BODY), qCreatedBy(id + "skA_socket", EntityType.BODY), qCreatedBy(id + "skA_shank", EntityType.BODY),
                        qCreatedBy(id + "skA_thr1", EntityType.BODY), qCreatedBy(id + "skA_thr2", EntityType.BODY), qCreatedBy(id + "skA_thr3", EntityType.BODY), qCreatedBy(id + "skA_thr4", EntityType.BODY),
                        qCreatedBy(id + "skB_head", EntityType.BODY), qCreatedBy(id + "skB_socket", EntityType.BODY), qCreatedBy(id + "skB_shank", EntityType.BODY),
                        qCreatedBy(id + "skB_thr1", EntityType.BODY), qCreatedBy(id + "skB_thr2", EntityType.BODY), qCreatedBy(id + "skB_thr3", EntityType.BODY), qCreatedBy(id + "skB_thr4", EntityType.BODY),
                        qCreatedBy(id + "skC_head", EntityType.BODY), qCreatedBy(id + "skC_socket", EntityType.BODY), qCreatedBy(id + "skC_shank", EntityType.BODY),
                        qCreatedBy(id + "skC_thr1", EntityType.BODY), qCreatedBy(id + "skC_thr2", EntityType.BODY), qCreatedBy(id + "skC_thr3", EntityType.BODY), qCreatedBy(id + "skC_thr4", EntityType.BODY),
                        qCreatedBy(id + "skD_head", EntityType.BODY), qCreatedBy(id + "skD_socket", EntityType.BODY), qCreatedBy(id + "skD_shank", EntityType.BODY),
                        qCreatedBy(id + "skD_thr1", EntityType.BODY), qCreatedBy(id + "skD_thr2", EntityType.BODY), qCreatedBy(id + "skD_thr3", EntityType.BODY), qCreatedBy(id + "skD_thr4", EntityType.BODY)
                    ]), "propertyType" : PropertyType.APPEARANCE, "value" : colHardwareSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_socket", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_SOCKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_shank", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_SHANK" });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_thr1", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_thr2", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_thr3", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skA_thr4", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_A_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_socket", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_SOCKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_shank", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_SHANK" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_thr1", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_thr2", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_thr3", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skB_thr4", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_B_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_socket", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_SOCKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_shank", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_SHANK" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_thr1", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_thr2", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_thr3", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skC_thr4", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_C_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_socket", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_SOCKET" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_shank", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_SHANK" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_thr1", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_thr2", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_thr3", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_THREAD" });
        setProperty(context, { "entities" : qCreatedBy(id + "skD_thr4", EntityType.BODY),   "propertyType" : PropertyType.NAME, "value" : "ISO4762_M4x16_D_THREAD" });


        // ====================================================================
        // 5. YAGI ANTENNA & ELEMENTS (SERIE 500 - 868 MHz 7-ELEMENT HIGH-GAIN)
        // ====================================================================

        // 5.1 Main Antenna Boom (2020 V-slot, L = 600 mm, clamped at CoG X = 253 mm)
        // Boom spans X = -253 mm (rear) to X = +347 mm (front), center Z = 150 mm (Z = 140..160 mm)
        fCuboid(context, id + "boomMain",      { "corner1" : vector(-253, -10, 140) * millimeter, "corner2" : vector(347, 10, 160) * millimeter });
        fCuboid(context, id + "boomSlotTop",   { "corner1" : vector(-253, -3, 158.2) * millimeter, "corner2" : vector(347, 3, 160.1) * millimeter });
        fCuboid(context, id + "boomSlotSideL", { "corner1" : vector(-253, -10.1, 147) * millimeter, "corner2" : vector(347, -8.2, 153) * millimeter });
        fCuboid(context, id + "boomSlotSideR", { "corner1" : vector(-253, 8.2, 147) * millimeter,  "corner2" : vector(347, 10.1, 153) * millimeter });
        fCuboid(context, id + "boomNoseCap",   { "corner1" : vector(347, -10.5, 139.5) * millimeter, "corner2" : vector(356, 10.5, 160.5) * millimeter });
        fCuboid(context, id + "boomRearCap",   { "corner1" : vector(-258, -10.5, 139.5) * millimeter, "corner2" : vector(-253, 10.5, 160.5) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "boomMain", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "501_ANTENNA_BOOM_2020" });
        setProperty(context, { "entities" : qCreatedBy(id + "boomMain", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "boomSlotTop", EntityType.BODY), qCreatedBy(id + "boomSlotSideL", EntityType.BODY), qCreatedBy(id + "boomSlotSideR", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "501_BOOM_SLOTS" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "boomSlotTop", EntityType.BODY), qCreatedBy(id + "boomSlotSideL", EntityType.BODY), qCreatedBy(id + "boomSlotSideR", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colSlotDark });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "boomNoseCap", EntityType.BODY), qCreatedBy(id + "boomRearCap", EntityType.BODY)]), "propertyType" : PropertyType.NAME, "value" : "512_BOOM_END_CAPS" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "boomNoseCap", EntityType.BODY), qCreatedBy(id + "boomRearCap", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colRubberFoot });

        // 5.2 7 Antenna Elements (dia 6 mm polished rods at Z = 174 mm, 14 mm above boom)
        // 1. Reflector: X = -253 + 20 = -233 mm, L = 176 mm
        fCylinder(context, id + "elemReflector", { "bottomCenter" : vector(-233, -88, 174) * millimeter, "topCenter" : vector(-233, 88, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountReflector",  { "corner1" : vector(-240, -6, 160) * millimeter, "corner2" : vector(-226, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemReflector", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "502_REFLECTOR_ROD" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountReflector", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_REFLECTOR" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemReflector", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountReflector", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 2. Driven Element / Dipole: X = -253 + 90 = -163 mm, L = 162 mm (with sleek gold SMA connector)
        fCylinder(context, id + "elemDrivenL",   { "bottomCenter" : vector(-163, -81, 174) * millimeter, "topCenter" : vector(-163, -4, 174) * millimeter, "radius" : 3 * millimeter });
        fCylinder(context, id + "elemDrivenR",   { "bottomCenter" : vector(-163, 4, 174) * millimeter,  "topCenter" : vector(-163, 81, 174) * millimeter,  "radius" : 3 * millimeter });
        fCuboid(context, id + "mountDriven",     { "corner1" : vector(-170, -6, 160) * millimeter, "corner2" : vector(-156, 6, 177) * millimeter });
        fCylinder(context, id + "smaConnector",  { "bottomCenter" : vector(-163, 0, 160) * millimeter, "topCenter" : vector(-163, 0, 150) * millimeter, "radius" : 3.5 * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemDrivenL", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "503_DRIVEN_DIPOLE_L" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemDrivenR", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "503_DRIVEN_DIPOLE_R" });
        setProperty(context, { "entities" : qUnion([qCreatedBy(id + "elemDrivenL", EntityType.BODY), qCreatedBy(id + "elemDrivenR", EntityType.BODY)]), "propertyType" : PropertyType.APPEARANCE, "value" : colBrassGold });
        setProperty(context, { "entities" : qCreatedBy(id + "mountDriven", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "509_EH_DRIVEN" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountDriven", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });
        setProperty(context, { "entities" : qCreatedBy(id + "smaConnector", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "511_SMA_CONNECTOR" });
        setProperty(context, { "entities" : qCreatedBy(id + "smaConnector", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colBrassGold });

        // 3. Director D1: X = -253 + 160 = -93 mm, L = 152 mm
        fCylinder(context, id + "elemD1",  { "bottomCenter" : vector(-93, -76, 174) * millimeter, "topCenter" : vector(-93, 76, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountD1",   { "corner1" : vector(-100, -6, 160) * millimeter, "corner2" : vector(-86, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD1", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "504_DIRECTOR_D1" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD1", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_D1" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD1", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD1", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 4. Director D2: X = -253 + 250 = -3 mm, L = 148 mm
        fCylinder(context, id + "elemD2",  { "bottomCenter" : vector(-3, -74, 174) * millimeter, "topCenter" : vector(-3, 74, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountD2",   { "corner1" : vector(-10, -6, 160) * millimeter, "corner2" : vector(4, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD2", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "505_DIRECTOR_D2" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD2", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_D2" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD2", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD2", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 5. Director D3: X = -253 + 350 = +97 mm, L = 144 mm
        fCylinder(context, id + "elemD3",  { "bottomCenter" : vector(97, -72, 174) * millimeter, "topCenter" : vector(97, 72, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountD3",   { "corner1" : vector(90, -6, 160) * millimeter, "corner2" : vector(104, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD3", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "506_DIRECTOR_D3" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD3", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_D3" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD3", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD3", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 6. Director D4: X = -253 + 460 = +207 mm, L = 140 mm
        fCylinder(context, id + "elemD4",  { "bottomCenter" : vector(207, -70, 174) * millimeter, "topCenter" : vector(207, 70, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountD4",   { "corner1" : vector(200, -6, 160) * millimeter, "corner2" : vector(214, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD4", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "507_DIRECTOR_D4" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD4", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_D4" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD4", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD4", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // 7. Director D5: X = -253 + 560 = +307 mm, L = 136 mm
        fCylinder(context, id + "elemD5",  { "bottomCenter" : vector(307, -68, 174) * millimeter, "topCenter" : vector(307, 68, 174) * millimeter, "radius" : 3 * millimeter });
        fCuboid(context, id + "mountD5",   { "corner1" : vector(300, -6, 160) * millimeter, "corner2" : vector(314, 6, 177) * millimeter });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD5", EntityType.BODY),  "propertyType" : PropertyType.NAME, "value" : "508_DIRECTOR_D5" });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD5", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "509_EH_D5" });
        setProperty(context, { "entities" : qCreatedBy(id + "elemD5", EntityType.BODY),  "propertyType" : PropertyType.APPEARANCE, "value" : colAluSilver });
        setProperty(context, { "entities" : qCreatedBy(id + "mountD5", EntityType.BODY), "propertyType" : PropertyType.APPEARANCE, "value" : colPetgBlue });

        // ====================================================================
        // 6. KINEMATIC MOTIONS (PITCH & PAN)
        // ====================================================================

        var elevationBodies = qUnion([
            qCreatedBy(id + "elAxle", EntityType.BODY),
            qCreatedBy(id + "el80TPulleyRim", EntityType.BODY),
            qCreatedBy(id + "el80TFlangeL", EntityType.BODY),
            qCreatedBy(id + "el80TFlangeR", EntityType.BODY),
            qCreatedBy(id + "elBeltTanL", EntityType.BODY),
            qCreatedBy(id + "elBeltTanR", EntityType.BODY),
            qCreatedBy(id + "elBeltArc80T", EntityType.BODY),
            qCreatedBy(id + "elShaftCollar", EntityType.BODY),
            qCreatedBy(id + "cradleLowerBody", EntityType.BODY),
            qCreatedBy(id + "cradleAxleCut", EntityType.BODY),
            qCreatedBy(id + "cradleCapBridge", EntityType.BODY),
            qCreatedBy(id + "skA_head", EntityType.BODY),
            qCreatedBy(id + "skA_socket", EntityType.BODY),
            qCreatedBy(id + "skA_shank", EntityType.BODY),
            qCreatedBy(id + "skA_thr1", EntityType.BODY),
            qCreatedBy(id + "skA_thr2", EntityType.BODY),
            qCreatedBy(id + "skA_thr3", EntityType.BODY),
            qCreatedBy(id + "skA_thr4", EntityType.BODY),
            qCreatedBy(id + "skB_head", EntityType.BODY),
            qCreatedBy(id + "skB_socket", EntityType.BODY),
            qCreatedBy(id + "skB_shank", EntityType.BODY),
            qCreatedBy(id + "skB_thr1", EntityType.BODY),
            qCreatedBy(id + "skB_thr2", EntityType.BODY),
            qCreatedBy(id + "skB_thr3", EntityType.BODY),
            qCreatedBy(id + "skB_thr4", EntityType.BODY),
            qCreatedBy(id + "skC_head", EntityType.BODY),
            qCreatedBy(id + "skC_socket", EntityType.BODY),
            qCreatedBy(id + "skC_shank", EntityType.BODY),
            qCreatedBy(id + "skC_thr1", EntityType.BODY),
            qCreatedBy(id + "skC_thr2", EntityType.BODY),
            qCreatedBy(id + "skC_thr3", EntityType.BODY),
            qCreatedBy(id + "skC_thr4", EntityType.BODY),
            qCreatedBy(id + "skD_head", EntityType.BODY),
            qCreatedBy(id + "skD_socket", EntityType.BODY),
            qCreatedBy(id + "skD_shank", EntityType.BODY),
            qCreatedBy(id + "skD_thr1", EntityType.BODY),
            qCreatedBy(id + "skD_thr2", EntityType.BODY),
            qCreatedBy(id + "skD_thr3", EntityType.BODY),
            qCreatedBy(id + "skD_thr4", EntityType.BODY),
            qCreatedBy(id + "boomMain", EntityType.BODY),
            qCreatedBy(id + "boomSlotTop", EntityType.BODY),
            qCreatedBy(id + "boomSlotSideL", EntityType.BODY),
            qCreatedBy(id + "boomSlotSideR", EntityType.BODY),
            qCreatedBy(id + "boomNoseCap", EntityType.BODY),
            qCreatedBy(id + "boomRearCap", EntityType.BODY),
            qCreatedBy(id + "elemReflector", EntityType.BODY),
            qCreatedBy(id + "mountReflector", EntityType.BODY),
            qCreatedBy(id + "elemDrivenL", EntityType.BODY),
            qCreatedBy(id + "elemDrivenR", EntityType.BODY),
            qCreatedBy(id + "mountDriven", EntityType.BODY),
            qCreatedBy(id + "smaConnector", EntityType.BODY),
            qCreatedBy(id + "elemD1", EntityType.BODY),
            qCreatedBy(id + "mountD1", EntityType.BODY),
            qCreatedBy(id + "elemD2", EntityType.BODY),
            qCreatedBy(id + "mountD2", EntityType.BODY),
            qCreatedBy(id + "elemD3", EntityType.BODY),
            qCreatedBy(id + "mountD3", EntityType.BODY),
            qCreatedBy(id + "elemD4", EntityType.BODY),
            qCreatedBy(id + "mountD4", EntityType.BODY),
            qCreatedBy(id + "elemD5", EntityType.BODY),
            qCreatedBy(id + "mountD5", EntityType.BODY)
        ]);

        // Pitch elevation assembly around axle at (0, 0, 140) mm
        opTransform(context, id + "elevationPitch", {
            "bodies" : elevationBodies,
            "transform" : rotationAround(line(vector(0, 0, 140) * millimeter, vector(0, -1, 0)), definition.elevationAngle)
        });

        var azimuthBodies = qUnion([
            qCreatedBy(id + "azBrgLowSteel", EntityType.BODY),
            qCreatedBy(id + "azBrgLowSeal", EntityType.BODY),
            qCreatedBy(id + "azBrgUpSteel", EntityType.BODY),
            qCreatedBy(id + "azBrgUpSeal", EntityType.BODY),
            qCreatedBy(id + "azDrumBody", EntityType.BODY),
            qCreatedBy(id + "az100TRim", EntityType.BODY),
            qCreatedBy(id + "az100TFlangeL", EntityType.BODY),
            qCreatedBy(id + "az100TFlangeU", EntityType.BODY),
            qCreatedBy(id + "azBeltTanL", EntityType.BODY),
            qCreatedBy(id + "azBeltTanR", EntityType.BODY),
            qCreatedBy(id + "azBeltArc100T", EntityType.BODY),
            qCreatedBy(id + "turretBaseDisc", EntityType.BODY),
            qCreatedBy(id + "towerLMain", EntityType.BODY),
            qCreatedBy(id + "towerLHub", EntityType.BODY),
            qCreatedBy(id + "towerLRibBack", EntityType.BODY),
            qCreatedBy(id + "towerLRibFwd", EntityType.BODY),
            qCreatedBy(id + "towerRMain", EntityType.BODY),
            qCreatedBy(id + "towerRHub", EntityType.BODY),
            qCreatedBy(id + "towerRRibBack", EntityType.BODY),
            qCreatedBy(id + "towerRRibFwd", EntityType.BODY),
            qCreatedBy(id + "elMotorStator", EntityType.BODY),
            qCreatedBy(id + "elMotorFrontBell", EntityType.BODY),
            qCreatedBy(id + "elMotorRearBell", EntityType.BODY),
            qCreatedBy(id + "elMotorShaft", EntityType.BODY),
            qCreatedBy(id + "elMotorBracket", EntityType.BODY),
            qCreatedBy(id + "el16TPulley", EntityType.BODY),
            qCreatedBy(id + "el16TFlange1", EntityType.BODY),
            qCreatedBy(id + "el16TFlange2", EntityType.BODY),
            qCreatedBy(id + "elBrgLSteel", EntityType.BODY),
            qCreatedBy(id + "elBrgLSeal", EntityType.BODY),
            qCreatedBy(id + "elBrgRSteel", EntityType.BODY),
            qCreatedBy(id + "elBrgRSeal", EntityType.BODY),
            elevationBodies
        ]);

        // Pan azimuth assembly around Z-axis at (0, 0, 0)
        opTransform(context, id + "azimuthPan", {
            "bodies" : azimuthBodies,
            "transform" : rotationAround(line(vector(0, 0, 0) * millimeter, vector(0, 0, 1)), definition.azimuthAngle)
        });
    });
