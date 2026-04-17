MSstatsPlateNormalize = function(input){
    plates = (input %>% distinct(Plate))[[1]]
    
    data = list()
    
    for (i in seq_along(plates)){
        temp = input %>% filter(Plate == plates[i])
        
        temp[, ABUNDANCE_RUN := median(Intensity, na.rm = TRUE),
             by = c("Run")]
        temp[, ABUNDANCE_FRACTION := median(ABUNDANCE_RUN, na.rm = TRUE)]
        temp[, Intensity := Intensity - ABUNDANCE_RUN + ABUNDANCE_FRACTION]
        temp = temp[, !(colnames(temp) %in% c("ABUNDANCE_RUN", 
                                              "ABUNDANCE_FRACTION")),
                    with = FALSE]
        
        data[[i]] = temp
    }
    
    data = rbindlist(data)
    
    data[, ABUNDANCE_RUN := median(Intensity, na.rm = TRUE),
         by = c("Run")]
    data[, ABUNDANCE_FRACTION := median(ABUNDANCE_RUN, na.rm = TRUE)]
    data[, Intensity := Intensity - ABUNDANCE_RUN + ABUNDANCE_FRACTION]
    data = data[, !(colnames(data) %in% c("ABUNDANCE_RUN",
                                          "ABUNDANCE_FRACTION")),
                with = FALSE]

    return(data)
}